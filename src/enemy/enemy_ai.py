"""Rule-Based AI Controller for Paper Warfire.
Operates under Fog of War compliance (No cheating).
Evaluates memory model, target scoring, movement towards strategic waypoints,
and coordinate bombardment.
"""

from typing import List, Tuple, Dict, Set, Optional
from collections import deque
import random

from src.core.constants import Team, GRID_COLS, GRID_ROWS
from src.game.config import UnitType
from src.game.command import Command, CommandType
from src.game.base_unit import BaseUnit
from src.game.battlefield import Battlefield
from src.game.fog_of_war import FogOfWarManager

class AIMemory:
    def __init__(self):
        # Maps unit_id -> (last_seen_x, last_seen_y, turn_seen)
        self.last_known_positions: Dict[str, Tuple[int, int, int]] = {}
        # List of suspected cluster coordinates
        self.suspected_clusters: List[Tuple[int, int]] = []
        # Strategic central waypoints to contest
        self.strategic_waypoints: List[Tuple[int, int]] = [
            (12, 4), (12, 8), (12, 12), (10, 6), (10, 10), (14, 6), (14, 10)
        ]

    def update_from_vision(
        self,
        battlefield: Battlefield,
        ai_fow: FogOfWarManager,
        current_turn: int
    ) -> List[BaseUnit]:
        """
        Discovers player units currently visible in AI's Fog of War.
        Updates last_known_positions.
        """
        visible_player_units: List[BaseUnit] = []
        for u in battlefield.units:
            if u.team == Team.PLAYER and u.is_alive:
                if ai_fow.is_visible(u.x, u.y):
                    visible_player_units.append(u)
                    self.last_known_positions[u.unit_id] = (u.x, u.y, current_turn)

        return visible_player_units


class EnemyAIController:
    def __init__(self, battlefield: Battlefield, ai_fow: FogOfWarManager):
        self.battlefield = battlefield
        self.ai_fow = ai_fow
        self.memory = AIMemory()

    def plan_turn(self, current_turn: int) -> List[Command]:
        """
        Generates one command per living enemy unit without cheating.
        """
        enemy_units = [u for u in self.battlefield.units if u.team == Team.ENEMY and u.is_alive]
        if not enemy_units:
            return []

        # 1. Update perception & memory from legal vision
        visible_players = self.memory.update_from_vision(self.battlefield, self.ai_fow, current_turn)

        # 2. Sort units by tactical priority (Artillery/Mortar -> Sniper -> Tank -> MG -> Pistol)
        def unit_priority(u: BaseUnit) -> int:
            order = {
                UnitType.ARTILLERY: 6,
                UnitType.MORTAR: 5,
                UnitType.SNIPER: 4,
                UnitType.TANK: 3,
                UnitType.MACHINE_GUN: 2,
                UnitType.PISTOL: 1
            }
            return order.get(u.unit_type, 0)

        sorted_enemies = sorted(enemy_units, key=unit_priority, reverse=True)

        commands: List[Command] = []
        claimed_destinations: Set[Tuple[int, int]] = set()

        for enemy in sorted_enemies:
            cmd = self._plan_unit_action(enemy, visible_players, claimed_destinations, current_turn)
            if cmd:
                enemy.assign_command(cmd)
                commands.append(cmd)
                if cmd.command_type == CommandType.MOVE:
                    claimed_destinations.add(cmd.target_coord)

        return commands

    def _plan_unit_action(
        self,
        unit: BaseUnit,
        visible_players: List[BaseUnit],
        claimed_destinations: Set[Tuple[int, int]],
        current_turn: int
    ) -> Command:
        # A. Combat Mode: If visible targets are in range, ATTACK
        attack_cmd = self._try_attack_visible_target(unit, visible_players)
        if attack_cmd:
            return attack_cmd

        # B. Low HP Retreat: If critically wounded (<= 25% HP), retreat eastward
        if unit.current_hp <= unit.max_hp * 0.25:
            retreat_cmd = self._try_retreat(unit, claimed_destinations)
            if retreat_cmd:
                return retreat_cmd

        # C. Advance towards visible target if out of range
        if visible_players:
            move_to_engage = self._move_towards_target(unit, visible_players[0], claimed_destinations)
            if move_to_engage:
                return move_to_engage

        # D. Blind Bombardment on last known position
        bombard_cmd = self._try_blind_bombardment(unit, current_turn)
        if bombard_cmd:
            return bombard_cmd

        # E. Patrol Mode: Advance towards strategic central waypoints
        patrol_cmd = self._patrol_towards_waypoints(unit, claimed_destinations)
        if patrol_cmd:
            return patrol_cmd

        # Fallback: Stay idle or hold ground
        return Command(unit_id=unit.unit_id, command_type=CommandType.IDLE, target_coord=(unit.x, unit.y))

    def _try_attack_visible_target(
        self,
        unit: BaseUnit,
        visible_players: List[BaseUnit]
    ) -> Optional[Command]:
        if not visible_players:
            return None

        # Score and pick best target in range
        best_target: Optional[BaseUnit] = None
        best_score = -9999.0

        for p in visible_players:
            dist = max(abs(unit.x - p.x), abs(unit.y - p.y))
            if dist <= unit.get_effective_attack_range():
                # Score formula: prioritize low HP + high threat - distance
                threat = getattr(p, "get_threat_score", lambda: 30.0)()
                score = (100 - p.current_hp) * 1.5 + threat - dist * 2.0
                if score > best_score:
                    best_score = score
                    best_target = p

        if best_target:
            return Command(
                unit_id=unit.unit_id,
                command_type=CommandType.ATTACK,
                target_coord=(best_target.x, best_target.y)
            )

        return None

    def _try_blind_bombardment(self, unit: BaseUnit, current_turn: int) -> Optional[Command]:
        """Artillery, Mortar, or Tank blind-bombarding last known player coordinates."""
        if unit.aoe_radius == 0:
            return None

        # Look for recent last known positions (within last 3 turns)
        candidates = [
            (pos_x, pos_y) for uid, (pos_x, pos_y, turn) in self.memory.last_known_positions.items()
            if current_turn - turn <= 3 and max(abs(unit.x - pos_x), abs(unit.y - pos_y)) <= unit.get_effective_attack_range()
        ]

        if candidates:
            target = candidates[0]
            return Command(
                unit_id=unit.unit_id,
                command_type=CommandType.ATTACK,
                target_coord=(target[0], target[1])
            )

        return None

    def _move_towards_target(
        self,
        unit: BaseUnit,
        target: BaseUnit,
        claimed: Set[Tuple[int, int]]
    ) -> Optional[Command]:
        reachable = self.battlefield.get_reachable_tiles(unit)
        if not reachable:
            return None

        best_tile = None
        min_dist = 9999

        for tx, ty in reachable:
            if (tx, ty) in claimed:
                continue
            dist_to_target = max(abs(tx - target.x), abs(ty - target.y))
            if dist_to_target < min_dist:
                min_dist = dist_to_target
                best_tile = (tx, ty)

        if best_tile and best_tile != (unit.x, unit.y):
            return Command(
                unit_id=unit.unit_id,
                command_type=CommandType.MOVE,
                target_coord=best_tile
            )

        return None

    def _try_retreat(self, unit: BaseUnit, claimed: Set[Tuple[int, int]]) -> Optional[Command]:
        reachable = self.battlefield.get_reachable_tiles(unit)
        if not reachable:
            return None

        # Retreat eastward towards enemy baseline (X = 23)
        best_tile = max(
            [t for t in reachable if t not in claimed],
            key=lambda t: t[0],
            default=None
        )

        if best_tile and best_tile != (unit.x, unit.y):
            return Command(
                unit_id=unit.unit_id,
                command_type=CommandType.MOVE,
                target_coord=best_tile
            )
        return None

    def _patrol_towards_waypoints(
        self,
        unit: BaseUnit,
        claimed: Set[Tuple[int, int]]
    ) -> Optional[Command]:
        reachable = self.battlefield.get_reachable_tiles(unit)
        if not reachable:
            return None

        # Pick nearest waypoint
        target_wp = min(
            self.memory.strategic_waypoints,
            key=lambda wp: abs(unit.x - wp[0]) + abs(unit.y - wp[1])
        )

        best_tile = None
        min_dist = 9999
        for tx, ty in reachable:
            if (tx, ty) in claimed:
                continue
            dist = abs(tx - target_wp[0]) + abs(ty - target_wp[1])
            if dist < min_dist:
                min_dist = dist
                best_tile = (tx, ty)

        if best_tile and best_tile != (unit.x, unit.y):
            return Command(
                unit_id=unit.unit_id,
                command_type=CommandType.MOVE,
                target_coord=best_tile
            )

        return None
