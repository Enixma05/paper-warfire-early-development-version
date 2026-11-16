import pytest
from src.core.constants import Team, Visibility
from src.game.config import UnitType, DEFAULT_UPGRADES
from src.game.command import CommandType
from src.game.battlefield import Battlefield
from src.game.fog_of_war import FogOfWarManager
from src.player.player_unit import PlayerUnit
from src.player.player_controller import PlayerController
from src.enemy.enemy_unit import EnemyUnit
from src.enemy.enemy_ai import EnemyAIController

def test_player_controller_movement_and_attack_assignment():
    bf = Battlefield(cols=24, rows=16, seed=42)
    fow = FogOfWarManager(cols=24, rows=16, team=Team.PLAYER)
    pc = PlayerController(bf, fow, starting_coins=150)

    p1 = PlayerUnit("p1", UnitType.PISTOL, 2, 2)
    bf.place_unit(p1, 2, 2)

    # Select unit
    selected = pc.select_unit_at(2, 2)
    assert selected == p1

    # Valid move assignment (within move range 4)
    success, msg = pc.assign_move_command((3, 2))
    assert success is True
    assert p1.planned_command is not None
    assert p1.planned_command.command_type == CommandType.MOVE
    assert p1.planned_command.target_coord == (3, 2)

    # Attack assignment (within attack range 6)
    success, msg = pc.assign_attack_command((6, 2))
    assert success is True
    assert p1.planned_command.command_type == CommandType.ATTACK
    assert p1.planned_command.target_coord == (6, 2)

    # Out of range attack (dist 10 > 6)
    success, msg = pc.assign_attack_command((12, 2))
    assert success is False

def test_player_controller_upgrade_purchase():
    bf = Battlefield(cols=24, rows=16, seed=42)
    fow = FogOfWarManager(cols=24, rows=16, team=Team.PLAYER)
    pc = PlayerController(bf, fow, starting_coins=150)

    tank = PlayerUnit("t1", UnitType.TANK, 2, 2)
    bf.place_unit(tank, 2, 2)

    # Buy Penetration (cost 120)
    success, msg = pc.buy_upgrade(tank, "penetration")
    assert success is True
    assert "penetration" in tank.upgrades
    assert pc.coins == 30

    # Cannot buy Scope (cost 100) because only 30 coins left
    success, msg = pc.buy_upgrade(tank, "scope")
    assert success is False
    assert pc.coins == 30

def test_enemy_ai_fog_of_war_compliance():
    bf = Battlefield(cols=24, rows=16, seed=42)
    ai_fow = FogOfWarManager(cols=24, rows=16, team=Team.ENEMY)
    ai = EnemyAIController(bf, ai_fow)

    # Place player at (1, 1) - hidden in AI fog
    player = PlayerUnit("p1", UnitType.PISTOL, 1, 1)
    # Place enemy sniper at (20, 10)
    enemy = EnemyUnit("e1", UnitType.SNIPER, 20, 10)
    bf.place_unit(player, 1, 1)
    bf.place_unit(enemy, 20, 10)

    ai_fow.update_visibility(bf.units)

    # Player is not visible to enemy
    assert ai_fow.is_visible(player.x, player.y) is False

    # AI plans turn
    commands = ai.plan_turn(current_turn=1)
    assert len(commands) == 1
    # AI must NOT attack hidden player directly, but patrol or move towards center
    cmd = commands[0]
    assert cmd.target_coord != (1, 1)

def test_enemy_ai_attacks_visible_target():
    bf = Battlefield(cols=24, rows=16, seed=42)
    ai_fow = FogOfWarManager(cols=24, rows=16, team=Team.ENEMY)
    ai = EnemyAIController(bf, ai_fow)

    # Place player and enemy on passable plains
    player = PlayerUnit("p1", UnitType.PISTOL, 18, 8)
    enemy = EnemyUnit("e1", UnitType.SNIPER, 20, 8)
    assert bf.place_unit(player, 18, 8) is True
    assert bf.place_unit(enemy, 20, 8) is True

    ai_fow.update_visibility(bf.units)

    # Player is now visible to enemy
    assert ai_fow.is_visible(player.x, player.y) is True

    # AI plans turn: should choose to ATTACK player
    commands = ai.plan_turn(current_turn=1)
    assert len(commands) == 1
    assert commands[0].command_type == CommandType.ATTACK
    assert commands[0].target_coord == (18, 8)
