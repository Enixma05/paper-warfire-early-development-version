"""Game Engine and Main Loop for Paper Warfire.
Implements the 60 FPS delta-time loop, event dispatching,
and decoupled rendering pipeline.
"""

import sys
import pygame
from typing import Optional

from src.core.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TARGET_FPS, WINDOW_TITLE,
    GameState, TurnSubState, Team, Visibility,
    COLOR_BG, COLOR_GRID, COLOR_ACCENT,
    COLOR_FOG_UNEXPLORED, COLOR_FOG_EXPLORED,
    COLOR_TERRAIN_PLAINS, COLOR_TERRAIN_FOREST, COLOR_TERRAIN_MOUNTAIN, COLOR_TERRAIN_WATER,
    GRID_COLS, GRID_ROWS, TILE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y
)
from src.game.config import TerrainType, CommandType
from src.core.state_manager import GameStateManager
from src.core.input_handler import InputHandler
from src.ui.font_manager import FontManager, VectorUnitRenderer
from src.ui.hud import InGameHUD
from src.ui.menu import MainMenu, PauseModal
from src.ui.game_over import GameOverScreen

class GameEngine:
    def __init__(self, headless: bool = False):
        self.headless = headless
        pygame.init()
        pygame.font.init()

        if not self.headless:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption(WINDOW_TITLE)
        else:
            self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()
        self.running = True

        self.state_mgr = GameStateManager()
        self.input_handler = InputHandler()
        self.hud: Optional[InGameHUD] = None

        # Modals & Screens
        self.main_menu = MainMenu(
            on_start=self.start_game,
            on_quit=self.quit_game
        )
        self.pause_modal = PauseModal(
            on_resume=self.resume_game,
            on_restart=self.restart_game,
            on_menu=self.return_to_menu
        )
        self.game_over_screen: Optional[GameOverScreen] = None

    def start_game(self) -> None:
        self.state_mgr.start_new_match()
        if self.state_mgr.session:
            self.hud = InGameHUD(self.state_mgr.session)
        self.input_handler.reset_camera()

    def resume_game(self) -> None:
        self.state_mgr.state = GameState.PLAYING

    def restart_game(self) -> None:
        self.start_game()

    def return_to_menu(self) -> None:
        self.state_mgr.state = GameState.MENU
        self.state_mgr.session = None
        self.hud = None

    def quit_game(self) -> None:
        self.running = False
        pygame.quit()
        sys.exit()

    def run(self) -> None:
        """Main 60 FPS Game Loop."""
        while self.running:
            dt = self.clock.tick(TARGET_FPS) / 1000.0

            self._process_events()
            self._update(dt)
            self._render()

            if not self.headless:
                pygame.display.flip()

    def _process_events(self) -> None:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.quit_game()

            curr_state = self.state_mgr.state
            if curr_state == GameState.MENU:
                self.main_menu.handle_event(event)

            elif curr_state == GameState.PLAYING:
                # Check for pause
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_p):
                    self.state_mgr.state = GameState.PAUSE
                    return

                # Pass to HUD
                if self.hud:
                    self.hud.handle_event(event)

                # Battlefield grid clicks
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.state_mgr.session:
                    mx, my = event.pos
                    # Ignore clicks on tactical panel (right 300px) and header/footer
                    if mx < SCREEN_WIDTH - 300 and 50 < my < SCREEN_HEIGHT - 30:
                        grid_pos = self.input_handler.screen_to_grid(mx, my)
                        if grid_pos:
                            self._handle_grid_click(grid_pos[0], grid_pos[1])

            elif curr_state == GameState.PAUSE:
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_p):
                    self.state_mgr.state = GameState.PLAYING
                else:
                    self.pause_modal.handle_event(event)

            elif curr_state in (GameState.VICTORY, GameState.DEFEAT):
                if not self.game_over_screen:
                    is_vic = (curr_state == GameState.VICTORY)
                    self.game_over_screen = GameOverScreen(
                        is_victory=is_vic,
                        session=self.state_mgr.session,
                        on_rematch=self.restart_game,
                        on_menu=self.return_to_menu
                    )
                self.game_over_screen.handle_event(event)

    def _handle_grid_click(self, gx: int, gy: int) -> None:
        sess = self.state_mgr.session
        if not sess or not self.hud:
            return

        ctrl = sess.player_ctrl

        # If currently in MOVE mode and a unit is selected, try assigning move to clicked tile
        if self.hud.current_action_mode == CommandType.MOVE and ctrl.selected_unit:
            success, msg = ctrl.assign_move_command((gx, gy))
            self.hud.status_feedback = msg
            if success:
                self.hud.current_action_mode = None
                self.hud.coord_input.clear()
            return

        # Otherwise, check if clicking on a friendly unit to select it
        unit = sess.battlefield.get_unit_at(gx, gy)
        if unit and unit.team == Team.PLAYER:
            ctrl.select_unit_at(gx, gy)
            self.hud.coord_input.clear()
            self.hud.status_feedback = f"Selected {unit.unit_type.value} [{unit.unit_id}]."
        else:
            # Clicking empty or enemy tile puts coordinate in the coordinate input box
            self.hud.coord_input.set_coordinate((gx, gy))

    def _update(self, dt: float) -> None:
        self.state_mgr.update(dt)

        if self.state_mgr.state == GameState.PLAYING:
            self.input_handler.update_camera(dt)

            # Check if state transitioned to game over
            if self.state_mgr.state in (GameState.VICTORY, GameState.DEFEAT):
                is_vic = (self.state_mgr.state == GameState.VICTORY)
                self.game_over_screen = GameOverScreen(
                    is_victory=is_vic,
                    session=self.state_mgr.session,
                    on_rematch=self.restart_game,
                    on_menu=self.return_to_menu
                )

    def _render(self) -> None:
        curr_state = self.state_mgr.state

        if curr_state == GameState.MENU:
            self.main_menu.render(self.screen)

        elif curr_state in (GameState.PLAYING, GameState.PAUSE):
            self.screen.fill(COLOR_BG)
            if self.state_mgr.session:
                self._render_battlefield()
                if self.hud:
                    self.hud.render(self.screen)

            if curr_state == GameState.PAUSE:
                self.pause_modal.render(self.screen)

        elif curr_state in (GameState.VICTORY, GameState.DEFEAT):
            if self.game_over_screen:
                self.game_over_screen.render(self.screen)

    def _render_battlefield(self) -> None:
        sess = self.state_mgr.session
        if not sess:
            return

        bf = sess.battlefield
        fow = sess.player_fow
        ctrl = sess.player_ctrl

        # 1. Render Terrain Tiles
        for x in range(bf.cols):
            for y in range(bf.rows):
                sx, sy = self.input_handler.grid_to_screen(x, y)
                if -TILE_SIZE <= sx < SCREEN_WIDTH - 290 and -TILE_SIZE <= sy < SCREEN_HEIGHT:
                    tile = bf.grid[x][y]
                    vis = fow.get_visibility(x, y)

                    if vis == Visibility.UNEXPLORED:
                        tile_col = COLOR_FOG_UNEXPLORED
                    elif vis == Visibility.EXPLORED:
                        tile_col = COLOR_FOG_EXPLORED
                    else:
                        if tile.terrain_type == TerrainType.FOREST:
                            tile_col = COLOR_TERRAIN_FOREST
                        elif tile.terrain_type == TerrainType.MOUNTAIN:
                            tile_col = COLOR_TERRAIN_MOUNTAIN
                        elif tile.terrain_type == TerrainType.WATER:
                            tile_col = COLOR_TERRAIN_WATER
                        else:
                            tile_col = COLOR_TERRAIN_PLAINS

                    pygame.draw.rect(self.screen, tile_col, (sx, sy, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(self.screen, COLOR_GRID, (sx, sy, TILE_SIZE, TILE_SIZE), 1)

        # 2. Movement Range Highlights (if unit selected and in MOVE mode)
        if ctrl.selected_unit and self.hud and self.hud.current_action_mode == CommandType.MOVE:
            reachable = bf.get_reachable_tiles(ctrl.selected_unit)
            for rx, ry in reachable:
                sx, sy = self.input_handler.grid_to_screen(rx, ry)
                highlight_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                highlight_surf.fill((242, 193, 78, 60))
                self.screen.blit(highlight_surf, (sx, sy))
                pygame.draw.rect(self.screen, COLOR_ACCENT, (sx, sy, TILE_SIZE, TILE_SIZE), 1)

        # 3. Render Units (Friendly units + Visible Enemy units)
        for unit in bf.units:
            if not unit.is_alive:
                continue

            # Check FoW visibility for enemy units
            if unit.team == Team.ENEMY and not fow.is_visible(unit.x, unit.y):
                continue

            sx, sy = self.input_handler.grid_to_screen(unit.x, unit.y)
            is_sel = (unit == ctrl.selected_unit)
            VectorUnitRenderer.draw_unit(self.screen, unit, sx, sy, is_selected=is_sel)

        # 4. Target reticle indicator (if coordinate entered in HUD)
        if self.hud and self.hud.coord_input.parsed_coord:
            tx, ty = self.hud.coord_input.parsed_coord
            sx, sy = self.input_handler.grid_to_screen(tx, ty)
            pygame.draw.rect(self.screen, (240, 80, 80), (sx, sy, TILE_SIZE, TILE_SIZE), 2)
            pygame.draw.circle(self.screen, (240, 80, 80), (sx + TILE_SIZE // 2, sy + TILE_SIZE // 2), 6, 2)

