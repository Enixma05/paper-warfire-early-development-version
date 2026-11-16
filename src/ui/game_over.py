"""Game Over Screen components for Paper Warfire.
Renders Victory Screen with match analytics and Defeat Screen with strategic tips.
"""

from typing import Callable, Optional
import pygame

from src.core.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BG, COLOR_TEXT, COLOR_TEXT_DIM,
    COLOR_ACCENT, COLOR_ENEMY, COLOR_PANEL_BG, COLOR_PANEL_BORDER, Team
)
from src.core.state_manager import MatchSession
from src.ui.font_manager import FontManager
from src.ui.hud import Button

class GameOverScreen:
    def __init__(self, is_victory: bool, session: Optional[MatchSession], on_rematch: Callable, on_menu: Callable):
        self.is_victory = is_victory
        self.session = session
        self.on_rematch = on_rematch
        self.on_menu = on_menu

        btn_w, btn_h = 220, 42
        cx = SCREEN_WIDTH // 2 - btn_w // 2
        cy = 480

        btn_color = (40, 110, 60) if is_victory else (100, 80, 40)
        btn_text = "MAIN LAGI (REMATCH)" if is_victory else "COBA LAGI (RETRY)"
        self.btn_rematch = Button(pygame.Rect(cx - 120, cy, btn_w, btn_h), btn_text, self.on_rematch, color=btn_color)
        self.btn_menu = Button(pygame.Rect(cx + 120, cy, btn_w, btn_h), "KEMBALI KE MENU", self.on_menu, color=(70, 75, 85))

    def handle_event(self, event: pygame.event.Event) -> None:
        self.btn_rematch.handle_event(event)
        self.btn_menu.handle_event(event)

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(COLOR_BG)

        # Subtle paper grid
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(surface, (40, 44, 52), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(surface, (40, 44, 52), (0, y), (SCREEN_WIDTH, y), 1)

        # Main Title Banner
        if self.is_victory:
            title = "★ KEMENANGAN TELAK! ★"
            subtitle = "Seluruh Kekuatan Lawan Telah Dieliminasi"
            banner_col = (80, 210, 120)
        else:
            title = "✖ PASUKAN ANDA KALAH ✖"
            subtitle = "Pertahanan Markas Tembus dan Pasukan Telah Gugur"
            banner_col = COLOR_ENEMY

        FontManager.render_text(surface, title, SCREEN_WIDTH // 2, 140, size=36, color=banner_col, center=True)
        FontManager.render_text(surface, subtitle, SCREEN_WIDTH // 2, 185, size=16, color=COLOR_TEXT_DIM, center=True)

        # Analytics Box
        box_w, box_h = 520, 220
        box_x = (SCREEN_WIDTH - box_w) // 2
        box_y = 230
        pygame.draw.rect(surface, COLOR_PANEL_BG, (box_x, box_y, box_w, box_h), border_radius=6)
        pygame.draw.rect(surface, COLOR_PANEL_BORDER, (box_x, box_y, box_w, box_h), 2, border_radius=6)

        FontManager.render_text(surface, "LAPORAN PERTEMPURAN", SCREEN_WIDTH // 2, box_y + 20, size=18, color=COLOR_ACCENT, center=True)

        if self.session:
            turns = self.session.current_turn
            survivors = len([u for u in self.session.battlefield.units if u.team == Team.PLAYER and u.is_alive])
            dead_enemies = len([u for u in self.session.war_result.destroyed_units if u.team == Team.ENEMY]) if self.session.war_result else 0
            fow_pct = int(self.session.player_fow.get_explored_ratio() * 100)
            coins = self.session.player_ctrl.coins

            stats = [
                f"• Jumlah Giliran Bertempur : {turns} Giliran",
                f"• Pasukan Kawan Bertahan   : {survivors} Unit",
                f"• Area Medan Terungkap (FoW) : {fow_pct}%",
                f"• Total Saldo Koin Sisa     : {coins} Koin",
            ]
            for i, line in enumerate(stats):
                FontManager.render_text(surface, line, box_x + 35, box_y + 60 + i * 28, size=14, color=COLOR_TEXT)
        else:
            FontManager.render_text(surface, "Data sesi pertempuran tidak tersedia.", SCREEN_WIDTH // 2, box_y + 80, size=14, color=COLOR_TEXT_DIM, center=True)

        # Tactical Tip on Defeat
        if not self.is_victory:
            tip = "Tips: Majukan Tank untuk menyerap damage dan intai artileri musuh dengan infanteri!"
            FontManager.render_text(surface, tip, SCREEN_WIDTH // 2, 445, size=13, color=(240, 190, 80), center=True)

        self.btn_rematch.render(surface)
        self.btn_menu.render(surface)

