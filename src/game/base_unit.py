"""BaseUnit implementation for all playable and enemy military units.
Handles stats, health pool, footprint, upgrades, and damage calculation.
"""

from typing import List, Tuple, Optional, Dict
from src.core.constants import Team
from src.game.config import UnitType, UnitStats, DEFAULT_UNIT_STATS, UpgradeItem
from src.game.command import Command

class BaseUnit:
    def __init__(
        self,
        unit_id: str,
        unit_type: UnitType,
        team: Team,
        x: int,
        y: int,
        custom_stats: Optional[UnitStats] = None
    ):
        self.unit_id = unit_id
        self.unit_type = unit_type
        self.team = team
        self.x = x
        self.y = y

        base_stats = custom_stats or DEFAULT_UNIT_STATS[unit_type]
        self.stats = base_stats
        self.current_hp = base_stats.max_hp
        self.is_alive = True
        self.planned_command: Optional[Command] = None
        self.upgrades: Dict[str, UpgradeItem] = {}

    @property
    def max_hp(self) -> int:
        return self.stats.max_hp

    @property
    def move_range(self) -> int:
        return self.stats.move_range

    @property
    def width(self) -> int:
        return self.stats.width

    @property
    def height(self) -> int:
        return self.stats.height

    @property
    def aoe_radius(self) -> int:
        return self.stats.aoe_radius

    def get_effective_attack_range(self) -> int:
        bonus = sum(up.range_bonus for up in self.upgrades.values())
        return self.stats.attack_range + bonus

    def get_effective_sight_range(self) -> int:
        bonus = sum(up.vision_bonus for up in self.upgrades.values())
        return self.stats.sight_range + bonus

    def get_effective_damage(self) -> int:
        boost_pct = sum(up.damage_boost_pct for up in self.upgrades.values())
        return int(round(self.stats.base_damage * (1.0 + boost_pct)))

    def get_occupied_tiles(self) -> List[Tuple[int, int]]:
        """Returns all grid tiles currently occupied by the unit footprint."""
        tiles = []
        for dx in range(self.width):
            for dy in range(self.height):
                tiles.append((self.x + dx, self.y + dy))
        return tiles

    def occupies_tile(self, tx: int, ty: int) -> bool:
        return (self.x <= tx < self.x + self.width) and (self.y <= ty < self.y + self.height)

    def apply_upgrade(self, upgrade: UpgradeItem) -> None:
        self.upgrades[upgrade.id] = upgrade

    def take_damage(self, raw_damage: int, terrain_defense_multiplier: float = 1.0) -> int:
        """
        Applies incoming damage taking into account terrain cover and natural armor.
        Formula: Final = Raw * Terrain_Cover * (1 - Armor_Mitigation)
        Returns the actual damage dealt.
        """
        if not self.is_alive:
            return 0

        mitigated = raw_damage * terrain_defense_multiplier * (1.0 - self.stats.armor_mitigation)
        actual_damage = max(1, int(round(mitigated)))

        self.current_hp = max(0, self.current_hp - actual_damage)
        if self.current_hp == 0:
            self.is_alive = False

        return actual_damage

    def assign_command(self, cmd: Optional[Command]) -> None:
        self.planned_command = cmd

    def clear_command(self) -> None:
        self.planned_command = None

    def __repr__(self) -> str:
        status = "ALIVE" if self.is_alive else "DEAD"
        return f"<{self.team.name} {self.unit_type.value} [{self.unit_id}] @({self.x},{self.y}) HP={self.current_hp}/{self.max_hp} {status}>"

