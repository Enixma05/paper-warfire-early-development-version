import pytest
from src.core.constants import Team
from src.game.config import UnitType, CommandType, GameRules, EconomyConfig
from src.game.command import Command
from src.game.battlefield import Battlefield
from src.game.fog_of_war import FogOfWarManager
from src.game.battle_resolver import BattleResolver
from src.player.player_unit import PlayerUnit
from src.enemy.enemy_unit import EnemyUnit

def test_win_condition_all_enemies_destroyed():
    bf = Battlefield(cols=24, rows=16, seed=42)
    fow = FogOfWarManager(cols=24, rows=16, team=Team.PLAYER)
    resolver = BattleResolver(bf)

    # 1 Player Sniper, 1 Enemy with 10 HP
    player = PlayerUnit("p1", UnitType.SNIPER, 2, 2)
    enemy = EnemyUnit("e1", UnitType.PISTOL, 4, 2)
    enemy.current_hp = 10  # low HP so sniper 1-shots it

    bf.place_unit(player, 2, 2)
    bf.place_unit(enemy, 4, 2)

    # Player attacks enemy
    player.assign_command(Command("p1", CommandType.ATTACK, (4, 2)))

    result = resolver.resolve_war_phase(fow)

    assert enemy in result.destroyed_units
    assert not enemy.is_alive
    assert enemy not in bf.units

    # Check victory check
    alive_enemies = [u for u in bf.units if u.team == Team.ENEMY and u.is_alive]
    alive_players = [u for u in bf.units if u.team == Team.PLAYER and u.is_alive]

    assert len(alive_enemies) == 0
    assert len(alive_players) == 1
    # Victory condition met!

def test_defeat_condition_all_players_destroyed():
    bf = Battlefield(cols=24, rows=16, seed=42)
    fow = FogOfWarManager(cols=24, rows=16, team=Team.PLAYER)
    resolver = BattleResolver(bf)

    # 1 Enemy Artillery, 1 Player with 10 HP
    enemy = EnemyUnit("e1", UnitType.ARTILLERY, 10, 2)
    player = PlayerUnit("p1", UnitType.PISTOL, 4, 2)
    player.current_hp = 10

    bf.place_unit(enemy, 10, 2)
    bf.place_unit(player, 4, 2)

    enemy.assign_command(Command("e1", CommandType.ATTACK, (4, 2)))

    result = resolver.resolve_war_phase(fow)

    assert player in result.destroyed_units
    assert not player.is_alive

    alive_players = [u for u in bf.units if u.team == Team.PLAYER and u.is_alive]
    assert len(alive_players) == 0
    # Defeat condition met!

def test_economy_rewards_from_kills():
    bf = Battlefield(cols=24, rows=16, seed=42)
    fow = FogOfWarManager(cols=24, rows=16, team=Team.PLAYER)
    resolver = BattleResolver(bf)

    # Player destroys enemy Tank (reward = 75 coins)
    player = PlayerUnit("p1", UnitType.ARTILLERY, 2, 2)
    enemy_tank = EnemyUnit("e_tank", UnitType.TANK, 6, 2)
    enemy_tank.current_hp = 10  # 1 hit away from death

    bf.place_unit(player, 2, 2)
    bf.place_unit(enemy_tank, 6, 2)

    player.assign_command(Command("p1", CommandType.ATTACK, (6, 2)))

    result = resolver.resolve_war_phase(fow)

    assert enemy_tank in result.destroyed_units
    assert result.coins_earned_from_kills == 75

