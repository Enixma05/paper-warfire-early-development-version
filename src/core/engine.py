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
    COLOR_BG, COLOR_GRID, COLOR_ACCENT, COLOR_TEXT, COLOR_TEXT_DIM,
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
        self.floating_texts: list = []  # Floating damage text feedback (BUG-006)
        self._last_processed_war_result = None

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

    def spawn_floating_text(self, gx: int, gy: int, text: str, color: tuple = (255, 90, 90)) -> None:
        """Spawns an animated combat damage or status popup above tile (gx, gy) (BUG-006)."""
        self.floating_texts.append({
            "gx": gx,
            "gy": gy,
            "text": text,
            "color": color,
            "timer": 2.2,
            "offset_y": 0.0
        })

    def _process_events(self) -> None:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.quit_game()

            curr_state = self.state_mgr.state
            if curr_state == GameState.MENU:
                self.main_menu.handle_event(event)

            elif curr_state == GameState.PLAYING:
                # Check if typing in coordinate box (BUG-002: prevent hotkey collision)
                coord_active = bool(self.hud and self.hud.coord_input.is_active)

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_p):
                        if coord_active:
                            if event.key == pygame.K_ESCAPE:
                                self.hud.coord_input.is_active = False
                            # Do not pause game while typing
                        else:
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

        # Check unit at clicked position
        clicked_unit = sess.battlefield.get_unit_at(gx, gy)
        if clicked_unit:
            if clicked_unit.team == Team.PLAYER:
                # Select friendly unit
                self.hud.inspected_enemy = None
                ctrl.select_unit_at(gx, gy)
                self.hud.coord_input.clear()
                self.hud.status_feedback = f"Selected {clicked_unit.unit_type.value} [{clicked_unit.unit_id}]."
            elif clicked_unit.team == Team.ENEMY and sess.player_fow.is_visible(clicked_unit.x, clicked_unit.y):
                # Visible enemy tapped! Display hostile stats in Inspector (BUG-011)
                self.hud.inspected_enemy = clicked_unit
                ctrl.deselect()
                self.hud.status_feedback = f"Inspecting enemy {clicked_unit.unit_type.value} [{clicked_unit.unit_id}]."
                self.hud.coord_input.set_coordinate((gx, gy))
            else:
                self.hud.inspected_enemy = None
                self.hud.coord_input.set_coordinate((gx, gy))
        else:
            self.hud.inspected_enemy = None
            self.hud.coord_input.set_coordinate((gx, gy))

    def _update(self, dt: float) -> None:
        self.state_mgr.update(dt)

        if self.state_mgr.state == GameState.PLAYING:
            # Disable WASD camera panning while user is typing in text box (BUG-002)
            coord_active = bool(self.hud and self.hud.coord_input.is_active)
            self.input_handler.update_camera(dt, disable_wasd=coord_active)

            # Spawn floating damage feedback when war phase resolves (BUG-006)
            sess = self.state_mgr.session
            if sess and sess.war_result and sess.war_result != self._last_processed_war_result:
                self._last_processed_war_result = sess.war_result
                for ce in sess.war_result.combat_events:
                    if ce.damage_dealt > 0 and ce.victim:
                        self.spawn_floating_text(ce.victim.x, ce.victim.y, f"-{ce.damage_dealt} DMG", (255, 75, 75))
                    elif not ce.victim:
                        self.spawn_floating_text(ce.target_coord[0], ce.target_coord[1], "MISS", (180, 185, 195))
                for me in sess.war_result.move_events:
                    if not me.success and me.clashed_with:
                        self.spawn_floating_text(me.to_coord[0], me.to_coord[1], "CLASH!", (240, 190, 60))

            # Update floating texts
            for ft in self.floating_texts:
                ft["timer"] -= dt
                ft["offset_y"] += 14.0 * dt
            self.floating_texts = [ft for ft in self.floating_texts if ft["timer"] > 0]

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

        # 1. Render Terrain Tiles with Fog of War (BUG-003 & BUG-009)
        for x in range(bf.cols):
            for y in range(bf.rows):
                sx, sy = self.input_handler.grid_to_screen(x, y)
                if -TILE_SIZE <= sx < SCREEN_WIDTH - 290 and -TILE_SIZE <= sy < SCREEN_HEIGHT:
                    tile = bf.grid[x][y]
                    vis = fow.get_visibility(x, y)

                    if vis == Visibility.UNEXPLORED:
                        tile_col = COLOR_FOG_UNEXPLORED
                        pygame.draw.rect(self.screen, tile_col, (sx, sy, TILE_SIZE, TILE_SIZE))
                        pygame.draw.rect(self.screen, (22, 25, 32), (sx, sy, TILE_SIZE, TILE_SIZE), 1)
                    else:
                        # Determine base terrain color
                        if tile.terrain_type == TerrainType.FOREST:
                            base_col = COLOR_TERRAIN_FOREST
                        elif tile.terrain_type == TerrainType.MOUNTAIN:
                            base_col = COLOR_TERRAIN_MOUNTAIN
                        elif tile.terrain_type == TerrainType.WATER:
                            base_col = COLOR_TERRAIN_WATER
                        else:
                            base_col = COLOR_TERRAIN_PLAINS

                        if vis == Visibility.EXPLORED:
                            # Shrouded terrain: dimmed, but terrain contour remains visible forever (BUG-003)
                            tile_col = (int(base_col[0] * 0.38), int(base_col[1] * 0.38), int(base_col[2] * 0.38))
                            pygame.draw.rect(self.screen, tile_col, (sx, sy, TILE_SIZE, TILE_SIZE))
                            pygame.draw.rect(self.screen, (40, 44, 52), (sx, sy, TILE_SIZE, TILE_SIZE), 1)
                        else:
                            # Full Visibility: bright terrain with geometric textures (BUG-009)
                            pygame.draw.rect(self.screen, base_col, (sx, sy, TILE_SIZE, TILE_SIZE))
                            pygame.draw.rect(self.screen, COLOR_GRID, (sx, sy, TILE_SIZE, TILE_SIZE), 1)

                            # Minimalist tactical terrain details
                            cx, cy = sx + TILE_SIZE // 2, sy + TILE_SIZE // 2
                            if tile.terrain_type == TerrainType.FOREST:
                                # Tree triangle icon
                                pts = [(cx, cy - 8), (cx - 7, cy + 6), (cx + 7, cy + 6)]
                                pygame.draw.polygon(self.screen, (42, 105, 55), pts)
                            elif tile.terrain_type == TerrainType.MOUNTAIN:
                                # Rocky peak triangle icon
                                pts = [(cx, cy - 9), (cx - 8, cy + 7), (cx + 8, cy + 7)]
                                pygame.draw.polygon(self.screen, (160, 165, 175), pts)
                                pygame.draw.line(self.screen, (90, 95, 105), (cx, cy - 9), (cx - 3, cy + 7), 2)
                            elif tile.terrain_type == TerrainType.WATER:
                                # Water waves
                                pygame.draw.line(self.screen, (70, 140, 200), (sx + 8, cy - 3), (sx + TILE_SIZE - 8, cy - 3), 2)
                                pygame.draw.line(self.screen, (70, 140, 200), (sx + 12, cy + 4), (sx + TILE_SIZE - 12, cy + 4), 2)

        # 2. Render Axis Labels (Col A-X on top, Row 1-16 on left) (BUG-007, BUG-010)
        for col_idx in range(bf.cols):
            hx, hy = self.input_handler.grid_to_screen(col_idx, 0)
            if -TILE_SIZE < hx < SCREEN_WIDTH - 300:
                col_label = chr(ord('A') + col_idx)
                FontManager.render_text(self.screen, col_label, hx + TILE_SIZE // 2, hy - 14, size=11, color=COLOR_TEXT_DIM, center=True)

        for row_idx in range(bf.rows):
            vx, vy = self.input_handler.grid_to_screen(0, row_idx)
            if 40 < vy < SCREEN_HEIGHT - 30:
                row_label = str(row_idx + 1)
                FontManager.render_text(self.screen, row_label, vx - 10, vy + TILE_SIZE // 2, size=11, color=COLOR_TEXT_DIM, center=True)

        # 3. Attack Range Highlight (BUG-005)
        if ctrl.selected_unit and self.hud and self.hud.current_action_mode == CommandType.ATTACK:
            max_rng = ctrl.selected_unit.get_effective_attack_range()
            for rx in range(bf.cols):
                for ry in range(bf.rows):
                    dist = max(abs(ctrl.selected_unit.x - rx), abs(ctrl.selected_unit.y - ry))
                    if dist <= max_rng:
                        asx, asy = self.input_handler.grid_to_screen(rx, ry)
                        if -TILE_SIZE <= asx < SCREEN_WIDTH - 290 and -TILE_SIZE <= asy < SCREEN_HEIGHT:
                            range_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                            range_surf.fill((242, 193, 78, 22))
                            self.screen.blit(range_surf, (asx, asy))
                            pygame.draw.rect(self.screen, (242, 193, 78, 80), (asx, asy, TILE_SIZE, TILE_SIZE), 1)

        # 4. Movement Range Highlights (if unit selected and in MOVE mode)
        if ctrl.selected_unit and self.hud and self.hud.current_action_mode == CommandType.MOVE:
            reachable = bf.get_reachable_tiles(ctrl.selected_unit)
            for rx, ry in reachable:
                sx, sy = self.input_handler.grid_to_screen(rx, ry)
                highlight_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                highlight_surf.fill((74, 144, 226, 70))
                self.screen.blit(highlight_surf, (sx, sy))
                pygame.draw.rect(self.screen, (100, 180, 255), (sx, sy, TILE_SIZE, TILE_SIZE), 1)

        # 5. Render Units (Friendly units + Visible Enemy units)
        for unit in bf.units:
            if not unit.is_alive:
                continue

            # Check FoW visibility for enemy units
            if unit.team == Team.ENEMY and not fow.is_visible(unit.x, unit.y):
                continue

            sx, sy = self.input_handler.grid_to_screen(unit.x, unit.y)
            is_sel = (unit == ctrl.selected_unit or (self.hud and unit == self.hud.inspected_enemy))
            VectorUnitRenderer.draw_unit(self.screen, unit, sx, sy, is_selected=is_sel)

        # 6. Target Reticle & AoE 3x3 Visualizer (BUG-005)
        if self.hud and self.hud.coord_input.parsed_coord:
            tx, ty = self.hud.coord_input.parsed_coord
            aoe = ctrl.selected_unit.aoe_radius if (ctrl.selected_unit and self.hud.current_action_mode == CommandType.ATTACK) else 0

            # Render 3x3 AoE splash area if unit has AoE
            if aoe > 0:
                for dx in range(-aoe, aoe + 1):
                    for dy in range(-aoe, aoe + 1):
                        ix, iy = tx + dx, ty + dy
                        if bf.is_valid_coord(ix, iy):
                            isx, isy = self.input_handler.grid_to_screen(ix, iy)
                            if -TILE_SIZE <= isx < SCREEN_WIDTH - 290 and -TILE_SIZE <= isy < SCREEN_HEIGHT:
                                is_center = (dx == 0 and dy == 0)
                                aoe_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                                aoe_color = (235, 60, 60, 80) if is_center else (245, 140, 40, 50)
                                aoe_surf.fill(aoe_color)
                                self.screen.blit(aoe_surf, (isx, isy))
                                pygame.draw.rect(self.screen, (240, 90, 70), (isx, isy, TILE_SIZE, TILE_SIZE), 1)

            # Center target reticle crosshair
            tsx, tsy = self.input_handler.grid_to_screen(tx, ty)
            pygame.draw.rect(self.screen, (250, 70, 70), (tsx, tsy, TILE_SIZE, TILE_SIZE), 2)
            pygame.draw.circle(self.screen, (250, 70, 70), (tsx + TILE_SIZE // 2, tsy + TILE_SIZE // 2), 7, 2)

            # In-Range / Out-of-Range Status Label
            if ctrl.selected_unit and self.hud.current_action_mode == CommandType.ATTACK:
                dist = max(abs(ctrl.selected_unit.x - tx), abs(ctrl.selected_unit.y - ty))
                in_range = dist <= ctrl.selected_unit.get_effective_attack_range()
                stat_text = "[IN RANGE]" if in_range else "[OUT OF RANGE]"
                stat_col = (80, 220, 100) if in_range else (250, 70, 70)
                FontManager.render_text(self.screen, stat_text, tsx + TILE_SIZE // 2, tsy - 12, size=11, color=stat_col, center=True)

        # 7. Render Floating Damage Text popups (BUG-006)
        for ft in self.floating_texts:
            fsx, fsy = self.input_handler.grid_to_screen(ft["gx"], ft["gy"])
            FontManager.render_text(
                self.screen,
                ft["text"],
                fsx + TILE_SIZE // 2,
                fsy - int(ft["offset_y"]),
                size=14,
                color=ft["color"],
                center=True
            )

