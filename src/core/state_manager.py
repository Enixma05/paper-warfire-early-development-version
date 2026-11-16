"""Finite State Machine (FSM) State Manager for Paper Warfire.
Coordinates global game states (MENU, PLAYING, PAUSE, VICTORY, DEFEAT)
and in-game WEGO turn sub-states (PLANNING, WAR_EXECUTION, SUMMARY).
"""

from typing import Dict, Any, Optional, Tuple, List
import pygame

from src.core.constants import (
    GameState, TurnSubState, Team, Visibility,
    COLOR_BG, COLOR_GRID, COLOR_PLAYER, COLOR_ENEMY, COLOR_ACCENT,
    COLOR_TEXT, COLOR_TEXT_DIM, COLOR_PANEL_BG, COLOR_PANEL_BORDER,
    COLOR_FOG_UNEXPLORED, COLOR_FOG_EXPLORED,
    COLOR_TERRAIN_PLAINS, COLOR_TERRAIN_FOREST, COLOR_TERRAIN_MOUNTAIN, COLOR_TERRAIN_WATER,
    GRID_COLS, GRID_ROWS, TILE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y
)
from src.game.config import UnitType, TerrainType, GameRules, EconomyConfig, DEFAULT_UPGRADES
from src.game.battlefield import Battlefield
from src.game.fog_of_war import FogOfWarManager
from src.game.battle_resolver import BattleResolver, WarPhaseResult
from src.player.player_unit import PlayerUnit
from src.player.player_controller import PlayerController
from src.enemy.enemy_unit import EnemyUnit
from src.enemy.enemy_ai import EnemyAIController

class MatchSession:
    """Encapsulates a single battlefield match lifecycle."""
    def __init__(self, seed: Optional[int] = None):
        self.battlefield = Battlefield(cols=GRID_COLS, rows=GRID_ROWS, seed=seed)
        self.player_fow = FogOfWarManager(cols=GRID_COLS, rows=GRID_ROWS, team=Team.PLAYER)
        self.enemy_fow = FogOfWarManager(cols=GRID_COLS, rows=GRID_ROWS, team=Team.ENEMY)
        self.player_ctrl = PlayerController(self.battlefield, self.player_fow, starting_coins=100)
        self.enemy_ai = EnemyAIController(self.battlefield, self.enemy_fow)
        self.resolver = BattleResolver(self.battlefield)
        self.rules = GameRules()
        self.econ = EconomyConfig()

        self.current_turn = 1
        self.turn_substate = TurnSubState.PLANNING
        self.planning_timer = self.rules.planning_turn_time_limit  # Countdown timer for planning phase (BUG-012)
        self.war_execution_timer = 0.0
        self.war_result: Optional[WarPhaseResult] = None
        self.match_log: List[str] = []

        # Setup standard initial armies
        self._spawn_initial_squads()
        # Initial vision update
        self.player_fow.update_visibility(self.battlefield.units)
        self.enemy_fow.update_visibility(self.battlefield.units)

    def _spawn_initial_squads(self) -> None:
        """Deploys standard squads on opposite sides of the battlefield.
        Guarantees deterministic, structured spawn positions (BUG-008).
        """
        # Ensure spawn zone tiles are passable Plains
        for x in range(4):
            for y in range(GRID_ROWS):
                self.battlefield.grid[x][y].terrain_type = TerrainType.PLAINS
        for x in range(GRID_COLS - 4, GRID_COLS):
            for y in range(GRID_ROWS):
                self.battlefield.grid[x][y].terrain_type = TerrainType.PLAINS

        # Player squad (Left side, Cols 1-2)
        player_roster = [
            (UnitType.PISTOL, 1, 3),
            (UnitType.MACHINE_GUN, 1, 6),
            (UnitType.TANK, 1, 9),
            (UnitType.SNIPER, 1, 13),
            (UnitType.MORTAR, 2, 4),
            (UnitType.ARTILLERY, 2, 11),
        ]
        for idx, (utype, qx, qy) in enumerate(player_roster):
            u = PlayerUnit(f"P_{utype.value}_{idx+1}", utype, qx, qy)
            self.battlefield.place_unit(u, qx, qy)

        # Enemy squad (Right side, Cols 20-22) - Deterministic deployment
        enemy_roster = [
            (UnitType.PISTOL, 22, 3),
            (UnitType.MACHINE_GUN, 22, 6),
            (UnitType.TANK, 20, 8),
            (UnitType.SNIPER, 22, 13),
            (UnitType.MORTAR, 21, 4),
            (UnitType.ARTILLERY, 20, 11),
        ]
        for idx, (utype, qx, qy) in enumerate(enemy_roster):
            u = EnemyUnit(f"E_{utype.value}_{idx+1}", utype, qx, qy)
            self.battlefield.place_unit(u, qx, qy)

    def start_war_phase(self) -> None:
        """Transitions from PLANNING to WAR_EXECUTION."""
        # 1. AI plans its commands
        self.enemy_ai.plan_turn(self.current_turn)
        # 2. Set substate and timer
        self.turn_substate = TurnSubState.WAR_EXECUTION
        self.war_execution_timer = 2.0  # 2.0 seconds animation/execution time
        # 3. Resolve simultaneous WEGO actions
        self.war_result = self.resolver.resolve_war_phase(self.player_fow, self.enemy_fow)

        # Log results
        for me in self.war_result.move_events:
            if not me.success and me.clashed_with:
                self.match_log.append(f"Clash! {me.unit.unit_id} bounced: {me.reason}")
        for ce in self.war_result.combat_events:
            if ce.victim:
                self.match_log.append(
                    f"{ce.attacker.unit_id} hit {ce.victim.unit_id} for {ce.damage_dealt} DMG ({ce.terrain_type_name})"
                )
        for du in self.war_result.destroyed_units:
            self.match_log.append(f"Unit Destroyed: {du.unit_id} ({du.team.name})")

    def end_war_phase(self) -> None:
        """Transitions from WAR_EXECUTION to SUMMARY."""
        self.turn_substate = TurnSubState.SUMMARY
        # Award base income + kills + recon
        turn_income = self.econ.base_turn_income
        kill_income = self.war_result.coins_earned_from_kills if self.war_result else 0
        recon_income = (self.war_result.revealed_tiles_count if self.war_result else 0) * self.econ.recon_tile_reward
        total_gained = turn_income + kill_income + recon_income
        self.player_ctrl.add_coins(total_gained)

    def advance_to_next_turn(self) -> None:
        """Advances turn counter and resets to PLANNING substate."""
        self.current_turn += 1
        self.turn_substate = TurnSubState.PLANNING
        self.planning_timer = self.rules.planning_turn_time_limit  # Reset countdown timer (BUG-012)
        self.war_result = None
        self.player_ctrl.deselect()
        self.player_fow.clear_temporary_reveals()
        self.enemy_fow.clear_temporary_reveals()
        self.player_fow.update_visibility(self.battlefield.units)
        self.enemy_fow.update_visibility(self.battlefield.units)

    def check_match_end(self) -> Optional[GameState]:
        """Evaluates absolute win/loss conditions."""
        alive_players = [u for u in self.battlefield.units if u.team == Team.PLAYER and u.is_alive]
        alive_enemies = [u for u in self.battlefield.units if u.team == Team.ENEMY and u.is_alive]

        if len(alive_enemies) == 0 and len(alive_players) > 0:
            return GameState.VICTORY
        if len(alive_players) == 0:
            return GameState.DEFEAT
        if self.current_turn > self.rules.max_turns:
            return GameState.DEFEAT

        return None


class GameStateManager:
    def __init__(self):
        self.state = GameState.MENU
        self.session: Optional[MatchSession] = None
        self.camera_x = 0
        self.camera_y = 0

    def start_new_match(self, seed: Optional[int] = None) -> None:
        self.session = MatchSession(seed=seed)
        self.state = GameState.PLAYING

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.state == GameState.MENU:
            # Menu event handling is plugged via UI
            pass
        elif self.state == GameState.PLAYING:
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_p):
                self.state = GameState.PAUSE
        elif self.state == GameState.PAUSE:
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_p):
                self.state = GameState.PLAYING

    def update(self, dt: float) -> None:
        if self.state == GameState.PLAYING and self.session:
            # Planning phase countdown timer (BUG-012)
            if self.session.turn_substate == TurnSubState.PLANNING:
                self.session.planning_timer -= dt
                if self.session.planning_timer <= 0.0:
                    self.session.planning_timer = 0.0
                    self.session.start_war_phase()

            elif self.session.turn_substate == TurnSubState.WAR_EXECUTION:
                self.session.war_execution_timer -= dt
                if self.session.war_execution_timer <= 0.0:
                    self.session.end_war_phase()
                    # Check match end after war phase
                    end_state = self.session.check_match_end()
                    if end_state:
                        self.state = end_state

