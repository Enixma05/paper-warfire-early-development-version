import pytest
from src.core.constants import Team
from src.game.config import UnitType, TerrainType
from src.game.command import Command, CommandType
from src.game.base_unit import BaseUnit
from src.game.battlefield import Battlefield
from src.game.fog_of_war import FogOfWarManager
from src.game.battle_resolver import BattleResolver

def test_simultaneous_movement_collision_clash():
    bf = Battlefield(cols=24, rows=16, seed=42)
    fow = FogOfWarManager(cols=24, rows=16, team=Team.PLAYER)
    resolver = BattleResolver(bf)

    # Player pistol at (2, 2), Enemy pistol at (4, 2)
    # Both order to move to (3, 2)
    p1 = BaseUnit("p1", UnitType.PISTOL, Team.PLAYER, 2, 2)
    p2 = BaseUnit("p2", UnitType.PISTOL, Team.ENEMY, 4, 2)
    bf.place_unit(p1, 2, 2)
    bf.place_unit(p2, 4, 2)

    p1.assign_command(Command("p1", CommandType.MOVE, (3, 2)))
    p2.assign_command(Command("p2", CommandType.MOVE, (3, 2)))

    hp_p1_before = p1.current_hp
    hp_p2_before = p2.current_hp

    result = resolver.resolve_war_phase(fow)

    # Collision should bounce both back to original positions
    assert p1.x == 2 and p1.y == 2
    assert p2.x == 4 and p2.y == 2

    # Both should have taken clash contact damage (10 damage)
    assert p1.current_hp == hp_p1_before - 10
    assert p2.current_hp == hp_p2_before - 10

def test_simultaneous_combat_and_aoe_falloff():
    bf = Battlefield(cols=24, rows=16, seed=42)
    fow = FogOfWarManager(cols=24, rows=16, team=Team.PLAYER)
    resolver = BattleResolver(bf)

    # Ensure plains terrain for predictable multipliers
    for x in range(24):
        for y in range(16):
            bf.grid[x][y].terrain_type = TerrainType.PLAINS

    # Mortar unit at (2, 2) fires AoE at (6, 2)
    mortar = BaseUnit("m1", UnitType.MORTAR, Team.PLAYER, 2, 2)
    # Target enemy at center (6, 2)
    enemy_center = BaseUnit("e_center", UnitType.PISTOL, Team.ENEMY, 6, 2)
    # Target enemy at adjacent tile (6, 3)
    enemy_edge = BaseUnit("e_edge", UnitType.PISTOL, Team.ENEMY, 6, 3)

    bf.place_unit(mortar, 2, 2)
    bf.place_unit(enemy_center, 6, 2)
    bf.place_unit(enemy_edge, 6, 3)

    mortar.assign_command(Command("m1", CommandType.ATTACK, (6, 2)))

    hp_center_before = enemy_center.current_hp
    hp_edge_before = enemy_edge.current_hp

    resolver.resolve_war_phase(fow)

    # Base damage of Mortar is 30
    # Center receives 100% = 30
    assert enemy_center.current_hp == hp_center_before - 30
    # Edge receives 50% falloff = 15
    assert enemy_edge.current_hp == hp_edge_before - 15

def test_terrain_defense_mitigation():
    bf = Battlefield(cols=24, rows=16, seed=42)
    fow = FogOfWarManager(cols=24, rows=16, team=Team.PLAYER)
    resolver = BattleResolver(bf)

    # Forest tile at (5, 5) provides 20% cover (0.8x)
    bf.grid[5][5].terrain_type = TerrainType.FOREST

    sniper = BaseUnit("s1", UnitType.SNIPER, Team.PLAYER, 1, 5)
    enemy_in_forest = BaseUnit("e_forest", UnitType.PISTOL, Team.ENEMY, 5, 5)
    bf.place_unit(sniper, 1, 5)
    bf.place_unit(enemy_in_forest, 5, 5)

    sniper.assign_command(Command("s1", CommandType.ATTACK, (5, 5)))
    hp_before = enemy_in_forest.current_hp

    resolver.resolve_war_phase(fow)

    # Sniper base damage = 60. In forest (0.8x), final = 48 damage
    assert enemy_in_forest.current_hp == hp_before - 48
