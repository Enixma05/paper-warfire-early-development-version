"""Unit Tests verifying fixes for issues reported in 1st Test (TEST_LOG.md).
Covers BUG-001 through BUG-013: AI bombardment fix, FoW permanence, Move > Attack resolution,
deterministic spawns, coordinate parsing, planning countdown timer, and phase locking.
"""

import pytest
from src.core.constants import Team, Visibility, TurnSubState, GRID_COLS, GRID_ROWS
from src.game.config import UnitType, CommandType, TerrainType
from src.game.command import Command
from src.game.battlefield import Battlefield
from src.game.fog_of_war import FogOfWarManager
from src.game.battle_resolver import BattleResolver
from src.player.player_unit import PlayerUnit
from src.enemy.enemy_unit import EnemyUnit
from src.enemy.enemy_ai import EnemyAIController
from src.core.state_manager import MatchSession, GameStateManager

def test_bug_001_blind_bombardment_tuple_unpacking():
    """BUG-001: Verifies that blind bombardment correctly unpacks (pos_x, pos_y) without NameError."""
    bf = Battlefield(cols=24, rows=16, seed=42)
    fow = FogOfWarManager(cols=24, rows=16, team=Team.ENEMY)
    ai = EnemyAIController(bf, fow)

    # Place artillery (aoe_radius=1, extreme range)
    artillery = EnemyUnit("e_arty", UnitType.ARTILLERY, 20, 10)
    bf.place_unit(artillery, 20, 10)

    # Insert a target position in memory (turn 1)
    ai.memory.last_known_positions["p_sniper"] = (5, 10, 1)

    # Simulate planning turn 2 (within 3 turns window)
    cmd = ai._try_blind_bombardment(artillery, current_turn=2)
    assert cmd is not None
    assert cmd.command_type == CommandType.ATTACK
    assert cmd.target_coord == (5, 10)


def test_bug_003_fog_of_war_permanence_on_unit_death():
    """BUG-003: Explored fog must never revert to UNEXPLORED when a unit dies."""
    fow = FogOfWarManager(cols=24, rows=16, team=Team.PLAYER)
    unit = PlayerUnit("p1", UnitType.PISTOL, 5, 5)

    # Initially unexplored
    assert fow.get_visibility(5, 5) == Visibility.UNEXPLORED

    # Unit reveals surrounding tiles
    fow.update_visibility([unit])
    assert fow.get_visibility(5, 5) == Visibility.VISIBLE
    assert fow.is_explored(5, 5) is True

    # Unit dies (is_alive = False)
    unit.is_alive = False
    fow.update_visibility([unit])

    # Tile must become EXPLORED (shrouded), NEVER UNEXPLORED!
    assert fow.get_visibility(5, 5) == Visibility.EXPLORED
    assert fow.is_explored(5, 5) is True
    assert fow.is_visible(5, 5) is False


def test_bug_004_move_resolves_before_attack():
    """BUG-004: Unit moves out of targeted tile; attack lands on original tile and misses moving victim."""
    bf = Battlefield(cols=24, rows=16, seed=42)
    fow = FogOfWarManager(cols=24, rows=16, team=Team.PLAYER)
    resolver = BattleResolver(bf)

    # Player at (2, 2) attacks tile (6, 2)
    attacker = PlayerUnit("p1", UnitType.SNIPER, 2, 2)
    # Enemy at (6, 2) moves to (6, 3)
    target = EnemyUnit("e1", UnitType.PISTOL, 6, 2)
    initial_hp = target.current_hp

    bf.place_unit(attacker, 2, 2)
    bf.place_unit(target, 6, 2)

    attacker.assign_command(Command("p1", CommandType.ATTACK, (6, 2)))
    target.assign_command(Command("e1", CommandType.MOVE, (6, 3)))

    result = resolver.resolve_war_phase(fow)

    # Verify target moved successfully to (6, 3)
    assert target.x == 6 and target.y == 3
    # Sniper single-target shot hit tile (6, 2), where no unit is present anymore
    assert target.current_hp == initial_hp


def test_bug_008_deterministic_spawn_zones():
    """BUG-008: Verifies deterministic initial squad placement in respective zones."""
    sess = MatchSession(seed=999)
    player_units = sess.player_ctrl.get_player_units()
    enemy_units = [u for u in sess.battlefield.units if u.team == Team.ENEMY]

    assert len(player_units) == 6
    assert len(enemy_units) == 6

    # All player units must spawn in West zone (Cols 1-3)
    for u in player_units:
        assert 0 <= u.x <= 3, f"Player unit {u.unit_id} spawned at column {u.x}"
        assert sess.battlefield.get_tile(u.x, u.y).terrain_type == TerrainType.PLAINS

    # All enemy units must spawn in East zone (Cols 20-23)
    for u in enemy_units:
        assert 20 <= u.x <= 23, f"Enemy unit {u.unit_id} spawned at column {u.x}"
        assert sess.battlefield.get_tile(u.x, u.y).terrain_type == TerrainType.PLAINS


def test_bug_009_terrain_diversity():
    """BUG-009: Central battlefield contains all 4 distinct terrain types."""
    bf = Battlefield(cols=24, rows=16, seed=123)
    terrains = {bf.grid[x][y].terrain_type for x in range(4, 20) for y in range(16)}

    assert TerrainType.PLAINS in terrains
    assert TerrainType.FOREST in terrains
    assert TerrainType.MOUNTAIN in terrains
    assert TerrainType.WATER in terrains


def test_bug_010_flexible_coordinate_parsing():
    """BUG-010: Validates 1-indexed boundary (24, 16), 0-indexed (0, 0, 14, 8), and alphanumeric (X16, H8, A1)."""
    assert Battlefield.parse_coordinate("H8") == (7, 7)
    assert Battlefield.parse_coordinate("A1") == (0, 0)
    assert Battlefield.parse_coordinate("X16") == (23, 15)
    assert Battlefield.parse_coordinate("0, 0") == (0, 0)
    assert Battlefield.parse_coordinate("14, 8") == (14, 8)
    assert Battlefield.parse_coordinate("24, 16") == (23, 15)  # Auto-mapped 1-indexed max edge


def test_bug_012_planning_phase_countdown_auto_lock():
    """BUG-012: Planning timer counts down and triggers War Phase on expiration."""
    state_mgr = GameStateManager()
    state_mgr.start_new_match(seed=42)
    sess = state_mgr.session

    assert sess.turn_substate == TurnSubState.PLANNING
    assert sess.planning_timer == sess.rules.planning_turn_time_limit

    # Advance time by 61 seconds
    state_mgr.update(61.0)

    # Must have transitioned to WAR_EXECUTION
    assert sess.turn_substate == TurnSubState.WAR_EXECUTION
