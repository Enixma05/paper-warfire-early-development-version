"""In-Game Heads-Up Display (HUD) for Paper Warfire.
Renders Top Status Header, Right Tactical Command Panel, Unit Inspector,
Command Queue list, and action buttons.
"""

from typing import Tuple, Optional, List, Callable
import pygame

from src.core.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_TEXT, COLOR_TEXT_DIM,
    COLOR_ACCENT, COLOR_PLAYER, COLOR_ENEMY, COLOR_PANEL_BG,
    COLOR_PANEL_BORDER, TurnSubState, Team
)
from src.game.config import CommandType, DEFAULT_UPGRADES
from src.player.player_unit import PlayerUnit
from src.player.player_controller import PlayerController
from src.core.state_manager import MatchSession
from src.ui.font_manager import FontManager
from src.ui.coord_input import CoordinateInputBox

class Button:
    def __init__(self, rect: pygame.Rect, text: str, callback: Callable, color: Tuple[int, int, int] = (45, 50, 60)):
        self.rect = rect
        self.text = text
        self.callback = callback
        self.color = color
        self.is_hovered = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()
                return True
        return False

    def render(self, surface: pygame.Surface, is_active: bool = False) -> None:
        bg = COLOR_ACCENT if is_active else ((60, 68, 82) if self.is_hovered else self.color)
        text_col = (20, 20, 25) if is_active else COLOR_TEXT

        pygame.draw.rect(surface, bg, self.rect, border_radius=3)
        pygame.draw.rect(surface, COLOR_PANEL_BORDER, self.rect, 1, border_radius=3)
        FontManager.render_text(surface, self.text, self.rect.centerx, self.rect.centery, size=14, color=text_col, center=True)


class InGameHUD:
    def __init__(self, session: MatchSession):
        self.session = session
        self.coord_input = CoordinateInputBox(SCREEN_WIDTH - 290, 250, width=170, height=28)
        self.current_action_mode: Optional[CommandType] = None
        self.status_feedback: str = ""

        # Setup persistent buttons
        panel_x = SCREEN_WIDTH - 300
        self.btn_move = Button(
            pygame.Rect(panel_x + 10, 200, 80, 28),
            "MOVE",
            lambda: self.set_action_mode(CommandType.MOVE)
        )
        self.btn_attack = Button(
            pygame.Rect(panel_x + 100, 200, 80, 28),
            "ATTACK",
            lambda: self.set_action_mode(CommandType.ATTACK)
        )
        self.btn_cancel_action = Button(
            pygame.Rect(panel_x + 190, 200, 85, 28),
            "CANCEL",
            self.cancel_selected_action
        )
        self.btn_confirm = Button(
            pygame.Rect(panel_x + 190, 250, 95, 28),
            "CONFIRM",
            self.confirm_current_action,
            color=(40, 100, 60)
        )
        self.btn_ready = Button(
            pygame.Rect(panel_x + 15, 630, 260, 36),
            "READY / END PLANNING",
            self.on_ready_clicked,
            color=(180, 130, 40)
        )

    def set_action_mode(self, mode: CommandType) -> None:
        self.current_action_mode = mode
        if mode == CommandType.MOVE:
            self.status_feedback = "Click a highlighted tile to set destination."
        elif mode == CommandType.ATTACK:
            self.status_feedback = "Type target coordinate (e.g. H8) & press Confirm."

    def cancel_selected_action(self) -> None:
        if self.session.player_ctrl.selected_unit:
            self.session.player_ctrl.cancel_unit_command(self.session.player_ctrl.selected_unit)
            self.status_feedback = "Unit command cleared."
        self.current_action_mode = None
        self.coord_input.clear()

    def confirm_current_action(self) -> None:
        ctrl = self.session.player_ctrl
        if not ctrl.selected_unit:
            self.status_feedback = "Select a friendly unit first!"
            return

        if self.current_action_mode == CommandType.ATTACK:
            target = self.coord_input.parsed_coord
            if target:
                success, msg = ctrl.assign_attack_command(target)
                self.status_feedback = msg
                if success:
                    self.current_action_mode = None
                    self.coord_input.clear()
            else:
                self.status_feedback = "Please input a valid coordinate (e.g. H8)."
        elif self.current_action_mode == CommandType.MOVE:
            target = self.coord_input.parsed_coord
            if target:
                success, msg = ctrl.assign_move_command(target)
                self.status_feedback = msg
                if success:
                    self.current_action_mode = None
                    self.coord_input.clear()

    def on_ready_clicked(self) -> None:
        if self.session.turn_substate == TurnSubState.PLANNING:
            self.session.start_war_phase()
            self.status_feedback = "Executing simultaneous orders..."
        elif self.session.turn_substate == TurnSubState.SUMMARY:
            self.session.advance_to_next_turn()
            self.status_feedback = f"Turn {self.session.current_turn} planning initiated."

    def handle_event(self, event: pygame.event.Event) -> None:
        # Pass to coordinate input box
        confirmed_coord = self.coord_input.handle_event(event)
        if confirmed_coord is not None:
            self.confirm_current_action()

        # Handle UI buttons
        self.btn_move.handle_event(event)
        self.btn_attack.handle_event(event)
        self.btn_cancel_action.handle_event(event)
        self.btn_confirm.handle_event(event)
        self.btn_ready.handle_event(event)

    def render(self, surface: pygame.Surface) -> None:
        self._render_header(surface)
        self._render_tactical_panel(surface)
        self._render_bottom_bar(surface)

    def _render_header(self, surface: pygame.Surface) -> None:
        # Header background
        header_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 50)
        pygame.draw.rect(surface, COLOR_PANEL_BG, header_rect)
        pygame.draw.line(surface, COLOR_PANEL_BORDER, (0, 50), (SCREEN_WIDTH, 50), 2)

        # Title
        FontManager.render_text(surface, "PAPER WARFIRE", 20, 15, size=20, color=COLOR_TEXT)

        # Turn Counter
        turn_str = f"TURN: {self.session.current_turn:02d} / {self.session.rules.max_turns}"
        FontManager.render_text(surface, turn_str, 200, 17, size=16, color=COLOR_ACCENT)

        # Phase Banner
        if self.session.turn_substate == TurnSubState.PLANNING:
            phase_text = "[ PLANNING PHASE ]"
            phase_col = COLOR_ACCENT
        elif self.session.turn_substate == TurnSubState.WAR_EXECUTION:
            phase_text = "[ WAR PHASE - EXECUTING... ]"
            phase_col = COLOR_ENEMY
        else:
            phase_text = "[ TURN SUMMARY ]"
            phase_col = (80, 200, 120)

        FontManager.render_text(surface, phase_text, 440, 17, size=16, color=phase_col, center=True)

        # Coin Wallet
        coin_str = f"COINS: {self.session.player_ctrl.coins}"
        FontManager.render_text(surface, coin_str, 680, 17, size=16, color=(240, 210, 60))

        # Squad Counters
        alive_players = len(self.session.player_ctrl.get_player_units())
        alive_enemies = len([u for u in self.session.battlefield.units if u.team == Team.ENEMY and u.is_alive])
        squad_str = f"UNITS: {alive_players} | HOSTILES: {alive_enemies}"
        FontManager.render_text(surface, squad_str, 840, 17, size=16, color=COLOR_TEXT_DIM)

    def _render_tactical_panel(self, surface: pygame.Surface) -> None:
        panel_x = SCREEN_WIDTH - 300
        panel_rect = pygame.Rect(panel_x, 50, 300, SCREEN_HEIGHT - 80)
        pygame.draw.rect(surface, COLOR_PANEL_BG, panel_rect)
        pygame.draw.line(surface, COLOR_PANEL_BORDER, (panel_x, 50), (panel_x, SCREEN_HEIGHT - 30), 2)

        # 1. Unit Inspector Section
        sel = self.session.player_ctrl.selected_unit
        FontManager.render_text(surface, "UNIT INSPECTOR", panel_x + 15, 60, size=14, color=COLOR_ACCENT)

        if sel:
            unit_title = f"{sel.unit_type.value} [{sel.unit_id}]"
            FontManager.render_text(surface, unit_title, panel_x + 15, 80, size=16, color=COLOR_TEXT)

            hp_str = f"HP: {sel.current_hp} / {sel.max_hp}"
            FontManager.render_text(surface, hp_str, panel_x + 15, 104, size=14, color=(100, 220, 120))

            stats_str = f"Move: {sel.move_range} | Range: {sel.get_effective_attack_range()}"
            FontManager.render_text(surface, stats_str, panel_x + 15, 124, size=13, color=COLOR_TEXT_DIM)

            dmg_str = f"Base DMG: {sel.get_effective_damage()} | AoE: {'3x3' if sel.aoe_radius else 'Single'}"
            FontManager.render_text(surface, dmg_str, panel_x + 15, 142, size=13, color=COLOR_TEXT_DIM)

            cmd_status = f"Order: {sel.planned_command}" if sel.planned_command else "Order: None"
            FontManager.render_text(surface, cmd_status, panel_x + 15, 162, size=12, color=COLOR_ACCENT)
        else:
            FontManager.render_text(surface, "No friendly unit selected.", panel_x + 15, 85, size=14, color=COLOR_TEXT_DIM)
            FontManager.render_text(surface, "Click any blue unit on the grid.", panel_x + 15, 110, size=12, color=COLOR_TEXT_DIM)

        # Action Buttons
        self.btn_move.render(surface, is_active=(self.current_action_mode == CommandType.MOVE))
        self.btn_attack.render(surface, is_active=(self.current_action_mode == CommandType.ATTACK))
        self.btn_cancel_action.render(surface)

        # Target input
        FontManager.render_text(surface, "MANUAL TARGET COORDINATE:", panel_x + 15, 232, size=12, color=COLOR_TEXT_DIM)
        self.coord_input.render(surface)
        self.btn_confirm.render(surface)

        # 2. Command Queue Section
        FontManager.render_text(surface, "PLANNED ORDERS QUEUE:", panel_x + 15, 310, size=14, color=COLOR_ACCENT)
        queue = self.session.player_ctrl.get_command_queue()
        qy = 332
        if queue:
            for u, cmd in queue[:6]:
                q_text = f"• {u.unit_type.value}: {cmd.command_type.name} -> {cmd.target_coord}"
                FontManager.render_text(surface, q_text, panel_x + 15, qy, size=12, color=COLOR_TEXT)
                qy += 18
        else:
            FontManager.render_text(surface, "No orders planned yet.", panel_x + 15, qy, size=12, color=COLOR_TEXT_DIM)

        # 3. Status feedback line
        if self.status_feedback:
            FontManager.render_text(surface, self.status_feedback, panel_x + 15, 595, size=11, color=(240, 200, 100))

        # Main Action Button (Ready / Next Turn)
        if self.session.turn_substate == TurnSubState.PLANNING:
            self.btn_ready.text = "READY / EXECUTE WAR PHASE"
            self.btn_ready.color = (180, 130, 40)
        elif self.session.turn_substate == TurnSubState.SUMMARY:
            self.btn_ready.text = "ADVANCE TO NEXT TURN"
            self.btn_ready.color = (40, 140, 80)
        else:
            self.btn_ready.text = "EXECUTING ORDERS..."
            self.btn_ready.color = (100, 40, 40)

        self.btn_ready.render(surface)

    def _render_bottom_bar(self, surface: pygame.Surface) -> None:
        bar_rect = pygame.Rect(0, SCREEN_HEIGHT - 30, SCREEN_WIDTH, 30)
        pygame.draw.rect(surface, (18, 20, 24), bar_rect)
        pygame.draw.line(surface, COLOR_PANEL_BORDER, (0, SCREEN_HEIGHT - 30), (SCREEN_WIDTH, SCREEN_HEIGHT - 30), 1)

        hint = "[L-CLICK] Select Unit / Tile  |  [WASD/Arrows] Pan Map  |  [ENTER] Confirm Target  |  [ESC/P] Pause Menu"
        FontManager.render_text(surface, hint, 20, SCREEN_HEIGHT - 22, size=13, color=COLOR_TEXT_DIM)

