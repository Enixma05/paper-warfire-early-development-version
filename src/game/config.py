"""Game balance configuration and data-driven mechanics.
Designed to be easily modified when design specs/documents are tweaked.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, Tuple
from src.game.command import Command, CommandType

class UnitType(Enum):
    PISTOL = "Pistol"
    MACHINE_GUN = "Machine Gun"
    SNIPER = "Sniper"
    TANK = "Tank"
    MORTAR = "Mortar"
    ARTILLERY = "Artillery"


@dataclass
class UnitStats:
    name: str
    unit_type: UnitType
    max_hp: int
    move_range: int
    attack_range: int
    base_damage: int
    aoe_radius: int  # 0 = single tile (1x1), 1 = 3x3 area
    width: int       # Tile footprint width
    height: int      # Tile footprint height
    sight_range: int # Vision range for Fog of War
    armor_mitigation: float = 0.0  # Natural armor (e.g. 0.10 for Tank)
    description: str = ""


# Default unit balance table based on GDD & combat specs
DEFAULT_UNIT_STATS: Dict[UnitType, UnitStats] = {
    UnitType.PISTOL: UnitStats(
        name="Pistol Unit",
        unit_type=UnitType.PISTOL,
        max_hp=70,
        move_range=4,
        attack_range=6,
        base_damage=25,
        aoe_radius=0,
        width=1,
        height=1,
        sight_range=4,
        armor_mitigation=0.0,
        description="Light infantry, fast scout, direct single-tile shot."
    ),
    UnitType.MACHINE_GUN: UnitStats(
        name="Machine Gun",
        unit_type=UnitType.MACHINE_GUN,
        max_hp=90,
        move_range=3,
        attack_range=8,
        base_damage=20,
        aoe_radius=1,  # 3x3 AoE
        width=1,
        height=1,
        sight_range=4,
        armor_mitigation=0.0,
        description="Area suppression unit, damages target and adjacent tiles."
    ),
    UnitType.SNIPER: UnitStats(
        name="Sniper Unit",
        unit_type=UnitType.SNIPER,
        max_hp=60,
        move_range=2,
        attack_range=12,
        base_damage=60,
        aoe_radius=0,
        width=1,
        height=1,
        sight_range=5,
        armor_mitigation=0.0,
        description="Long range marksman, high single-target burst damage."
    ),
    UnitType.TANK: UnitStats(
        name="Tank Unit",
        unit_type=UnitType.TANK,
        max_hp=200,
        move_range=3,
        attack_range=15,
        base_damage=50,  # 40-60 range avg
        aoe_radius=1,  # 3x3 AoE
        width=2,
        height=2,      # Footprint representation
        sight_range=4,
        armor_mitigation=0.10,  # 10% damage reduction
        description="Heavy vanguard, absorbs damage with AoE cannon fire."
    ),
    UnitType.MORTAR: UnitStats(
        name="Mortar Unit",
        unit_type=UnitType.MORTAR,
        max_hp=100,
        move_range=2,
        attack_range=18,
        base_damage=30,
        aoe_radius=1,  # 3x3 AoE
        width=1,
        height=2,
        sight_range=4,
        armor_mitigation=0.0,
        description="Mid-range artillery, arced trajectory over obstacles."
    ),
    UnitType.ARTILLERY: UnitStats(
        name="Artillery Unit",
        unit_type=UnitType.ARTILLERY,
        max_hp=120,
        move_range=1,
        attack_range=25,
        base_damage=70,
        aoe_radius=1,  # 3x3 AoE
        width=2,
        height=2,
        sight_range=3,
        armor_mitigation=0.0,
        description="Heavy siege weapon, extreme range bombardment."
    ),
}


class TerrainType(Enum):
    PLAINS = "Plains"
    FOREST = "Forest"
    MOUNTAIN = "Mountain"
    WATER = "Water"


@dataclass
class TerrainStats:
    name: str
    terrain_type: TerrainType
    move_cost: float
    defense_multiplier: float  # Multiplier on incoming damage (lower = more cover)
    is_passable: bool
    blocks_vision: bool


DEFAULT_TERRAIN_STATS: Dict[TerrainType, TerrainStats] = {
    TerrainType.PLAINS: TerrainStats(
        name="Plains / Grass",
        terrain_type=TerrainType.PLAINS,
        move_cost=1.0,
        defense_multiplier=1.0,
        is_passable=True,
        blocks_vision=False
    ),
    TerrainType.FOREST: TerrainStats(
        name="Forest / Trees",
        terrain_type=TerrainType.FOREST,
        move_cost=2.0,
        defense_multiplier=0.8,  # 20% cover reduction
        is_passable=True,
        blocks_vision=True
    ),
    TerrainType.MOUNTAIN: TerrainStats(
        name="Mountain / Rocks",
        terrain_type=TerrainType.MOUNTAIN,
        move_cost=999.0,         # Impassable
        defense_multiplier=0.6,  # 40% cover reduction
        is_passable=False,
        blocks_vision=True
    ),
    TerrainType.WATER: TerrainStats(
        name="Water / Swamp",
        terrain_type=TerrainType.WATER,
        move_cost=2.0,
        defense_multiplier=1.2,  # +20% damage vulnerability
        is_passable=True,
        blocks_vision=False
    ),
}


@dataclass
class EconomyConfig:
    base_turn_income: int = 50
    kill_rewards: Dict[UnitType, int] = field(default_factory=lambda: {
        UnitType.PISTOL: 25,
        UnitType.MACHINE_GUN: 40,
        UnitType.SNIPER: 40,
        UnitType.TANK: 75,
        UnitType.MORTAR: 75,
        UnitType.ARTILLERY: 75,
    })
    recon_tile_reward: int = 1  # Coins per newly revealed tile


@dataclass
class UpgradeItem:
    id: str
    name: str
    cost: int
    description: str
    damage_boost_pct: float = 0.0     # e.g. 0.15 (+15%)
    range_bonus: int = 0              # e.g. +2 attack range
    vision_bonus: int = 0             # e.g. +1 sight range
    aoe_falloff_mitigation: float = 0.0 # Reduces distance falloff penalty


DEFAULT_UPGRADES: Dict[str, UpgradeItem] = {
    "penetration": UpgradeItem(
        id="penetration",
        name="Penetration Shells",
        cost=120,
        description="+15% damage to attacks",
        damage_boost_pct=0.15
    ),
    "scope": UpgradeItem(
        id="scope",
        name="Extended Scope",
        cost=100,
        description="+2 attack range, +1 vision range",
        range_bonus=2,
        vision_bonus=1
    ),
    "magazine": UpgradeItem(
        id="magazine",
        name="High-Capacity Magazine",
        cost=90,
        description="Reduces AoE edge damage penalty by 20%",
        aoe_falloff_mitigation=0.20
    ),
    "scan_drone": UpgradeItem(
        id="scan_drone",
        name="Scan Drone",
        cost=80,
        description="Reveals a 5x5 tile area for 1 turn (Consumable)"
    )
}


@dataclass
class GameRules:
    max_turns: int = 25
    planning_turn_time_limit: float = 60.0  # Seconds allowed for planning per turn (BUG-012)
    contact_damage_on_collision: int = 10
    aoe_falloff_center_mult: float = 1.0
    aoe_falloff_surround_mult: float = 0.5
