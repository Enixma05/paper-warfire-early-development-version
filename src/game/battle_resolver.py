"""Battle Resolver for Paper Warfire.
Executes the simultaneous WEGO resolution loop:
Movement (Collision/Clash) -> Recon -> Simultaneous Combat (AoE Falloff) -> Casualty -> Impact Fog Reveal.
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Set, Optional

from src.core.constants import Team
from src.game.config import GameRules
from src.game.command import Command, CommandType
from src.game.base_unit import BaseUnit
from src.game.battlefield import Battlefield
from src.game.fog_of_war import FogOfWarManager

@dataclass
class CombatHitEvent:
    attacker: BaseUnit
    target_coord: Tuple[int, int]
    victim: Optional[BaseUnit]
    damage_dealt: int
    is_center: bool
    terrain_type_name: str


@dataclass
class MoveEvent:
    unit: BaseUnit
    from_coord: Tuple[int, int]
    to_coord: Tuple[int, int]
    success: bool
    clashed_with: Optional[BaseUnit] = None
    reason: str = ""


@dataclass
class WarPhaseResult:
    move_events: List[MoveEvent] = field(default_factory=list)
    combat_events: List[CombatHitEvent] = field(default_factory=list)
    destroyed_units: List[BaseUnit] = field(default_factory=list)
    coins_earned_from_kills: int = 0
    revealed_tiles_count: int = 0
    impact_coords: List[Tuple[int, int]] = field(default_factory=list)


class BattleResolver:
    def __init__(self, battlefield: Battlefield, rules: Optional[GameRules] = None):
        self.battlefield = battlefield
        self.rules = rules or GameRules()

    def resolve_war_phase(
        self,
        player_fow: FogOfWarManager,
        enemy_fow: Optional[FogOfWarManager] = None
    ) -> WarPhaseResult:
        result = WarPhaseResult()

        # Step 1: Resolve Movement
        self._resolve_movement(result)

        # Step 2: Recon / Vision Update
        new_tiles = player_fow.update_visibility(self.battlefield.units)
        result.revealed_tiles_count += new_tiles
        if enemy_fow:
            enemy_fow.update_visibility(self.battlefield.units)

        # Step 3: Simultaneous Combat & Firing
        self._resolve_combat(result)

        # Step 4: Casualty Resolution
        self._resolve_casualties(result)

        # Step 5: Fog of War Impact Reveal
        for ix, iy in result.impact_coords:
            player_fow.reveal_area(ix, iy, radius=1)
            if enemy_fow:
                enemy_fow.reveal_area(ix, iy, radius=1)

        # Clean up unit commands for next turn
        for u in self.battlefield.units:
            u.clear_command()

        return result

    def _resolve_movement(self, result: WarPhaseResult) -> None:
        """
        Processes simultaneous movement with collision detection (bouncing clash & ambush).
        """
        move_orders: List[Tuple[BaseUnit, Tuple[int, int]]] = []
        for u in self.battlefield.units:
            if u.is_alive and u.planned_command and u.planned_command.command_type == CommandType.MOVE:
                dest = u.planned_command.target_coord
                move_orders.append((u, dest))

        # Check for destination collisions (two or more units moving to the exact same destination)
        dest_claims: Dict[Tuple[int, int], List[BaseUnit]] = {}
        for u, dest in move_orders:
            dest_claims.setdefault(dest, []).append(u)

        resolved_destinations: Dict[BaseUnit, Tuple[int, int]] = {}

        for dest, units in dest_claims.items():
            if len(units) > 1:
                # Head-on collision! All colliding units clash and bounce back
                for u in units:
                    dmg = u.take_damage(self.rules.contact_damage_on_collision)
                    result.move_events.append(
                        MoveEvent(
                            unit=u,
                            from_coord=(u.x, u.y),
                            to_coord=(u.x, u.y),
                            success=False,
                            clashed_with=units[0] if units[0] != u else units[1],
                            reason=f"Head-on collision at {dest}! Received {dmg} clash damage."
                        )
                    )
            else:
                unit = units[0]
                # Check if destination tile is occupied by an immobile or staying unit
                curr_occupant = self.battlefield.get_unit_at(dest[0], dest[1])
                is_curr_occupant_moving = any(u == curr_occupant for u, _ in move_orders)

                # Validate reachable and bounds
                reachable = self.battlefield.get_reachable_tiles(unit)
                if dest in reachable and (curr_occupant is None or is_curr_occupant_moving):
                    resolved_destinations[unit] = dest
                else:
                    result.move_events.append(
                        MoveEvent(
                            unit=unit,
                            from_coord=(unit.x, unit.y),
                            to_coord=(unit.x, unit.y),
                            success=False,
                            reason="Blocked destination or out of range."
                        )
                    )

        # Apply successful moves to battlefield
        for unit, dest in resolved_destinations.items():
            old_coord = (unit.x, unit.y)
            self.battlefield.place_unit(unit, dest[0], dest[1])
            result.move_events.append(
                MoveEvent(
                    unit=unit,
                    from_coord=old_coord,
                    to_coord=dest,
                    success=True,
                    reason="Moved successfully."
                )
            )

    def _resolve_combat(self, result: WarPhaseResult) -> None:
        """
        Executes simultaneous weapon firing and queues damage before applying it.
        """
        damage_queue: List[Tuple[BaseUnit, int, CombatHitEvent]] = []

        for attacker in self.battlefield.units:
            if not attacker.is_alive or not attacker.planned_command:
                continue

            if attacker.planned_command.command_type != CommandType.ATTACK:
                continue

            target_x, target_y = attacker.planned_command.target_coord
            result.impact_coords.append((target_x, target_y))

            # Range check (Chebyshev distance)
            dist = max(abs(attacker.x - target_x), abs(attacker.y - target_y))
            if dist > attacker.get_effective_attack_range():
                continue

            base_dmg = attacker.get_effective_damage()
            aoe_radius = attacker.aoe_radius

            # Determine affected tiles
            impact_tiles: List[Tuple[int, int, bool]] = []  # (x, y, is_center)
            if aoe_radius == 0:
                impact_tiles.append((target_x, target_y, True))
            else:
                for dx in range(-aoe_radius, aoe_radius + 1):
                    for dy in range(-aoe_radius, aoe_radius + 1):
                        ix, iy = target_x + dx, target_y + dy
                        if self.battlefield.is_valid_coord(ix, iy):
                            is_center = (dx == 0 and dy == 0)
                            impact_tiles.append((ix, iy, is_center))

            # Check damage on each impacted tile
            hit_units_this_attack: Set[BaseUnit] = set()
            for ix, iy, is_center in impact_tiles:
                victim = self.battlefield.get_unit_at(ix, iy)
                if victim and victim.is_alive and victim != attacker:
                    if victim in hit_units_this_attack:
                        # Avoid multi-hitting same unit footprint multiple times per attack
                        continue
                    hit_units_this_attack.add(victim)

                    # Calculate falloff
                    if is_center:
                        falloff = self.rules.aoe_falloff_center_mult
                    else:
                        falloff = self.rules.aoe_falloff_surround_mult
                        # Magazine upgrade bonus
                        mag_bonus = sum(u.aoe_falloff_mitigation for u in attacker.upgrades.values())
                        falloff = min(1.0, falloff + mag_bonus)

                    tile = self.battlefield.get_tile(ix, iy)
                    terrain_cover = tile.stats.defense_multiplier if tile else 1.0

                    raw_damage = int(round(base_dmg * falloff))
                    evt = CombatHitEvent(
                        attacker=attacker,
                        target_coord=(ix, iy),
                        victim=victim,
                        damage_dealt=raw_damage,
                        is_center=is_center,
                        terrain_type_name=tile.terrain_type.value if tile else "Plains"
                    )
                    damage_queue.append((victim, raw_damage, evt))
                elif not victim:
                    # Missed shot on empty tile (still recorded for visual and FoW impact)
                    tile = self.battlefield.get_tile(ix, iy)
                    evt = CombatHitEvent(
                        attacker=attacker,
                        target_coord=(ix, iy),
                        victim=None,
                        damage_dealt=0,
                        is_center=is_center,
                        terrain_type_name=tile.terrain_type.value if tile else "Plains"
                    )
                    result.combat_events.append(evt)

        # Simultaneously apply all queued damage
        for victim, raw_dmg, evt in damage_queue:
            tile = self.battlefield.get_tile(victim.x, victim.y)
            cover = tile.stats.defense_multiplier if tile else 1.0
            actual = victim.take_damage(raw_dmg, terrain_defense_multiplier=cover)
            evt.damage_dealt = actual
            result.combat_events.append(evt)

    def _resolve_casualties(self, result: WarPhaseResult) -> None:
        """Removes dead units from grid and awards kill bounty to player."""
        from src.game.config import EconomyConfig
        econ = EconomyConfig()

        for u in list(self.battlefield.units):
            if not u.is_alive:
                result.destroyed_units.append(u)
                self.battlefield.remove_unit(u)
                if u.team == Team.ENEMY:
                    reward = econ.kill_rewards.get(u.unit_type, 40)
                    result.coins_earned_from_kills += reward
