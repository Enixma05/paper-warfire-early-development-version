"""Menu UI components for Paper Warfire.
Implements Main Menu, Pause Screen Modal, and How to Play multi-tab educational guide.
"""

from typing import Callable, Optional
import sys
import pygame

from src.core.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BG, COLOR_TEXT, COLOR_TEXT_DIM,
    COLOR_ACCENT, COLOR_PANEL_BG, COLOR_PANEL_BORDER
)
from src.ui.font_manager import FontManager
from src.ui.hud import Button

class MainMenu:
    def __init__(self, on_start: Callable, on_quit: Callable):
        self.on_start = on_start
        self.on_quit = on_quit
        self.show_how_to_play = False
        self.how_to_play_tab = 1

        btn_w, btn_h = 240, 44
        cx = SCREEN_WIDTH // 2 - btn_w // 2
        self.btn_start = Button(pygame.Rect(cx, 320, btn_w, btn_h), "START BATTLE", self.on_start, color=(40, 110, 60))
        self.btn_how_to_play = Button(pygame.Rect(cx, 380, btn_w, btn_h), "HOW TO PLAY", self._toggle_how_to_play, color=(45, 60, 85))
        self.btn_quit = Button(pygame.Rect(cx, 440, btn_w, btn_h), "QUIT GAME", self.on_quit, color=(90, 40, 40))

        # Close button for modal
        self.btn_close_help = Button(pygame.Rect(SCREEN_WIDTH // 2 - 60, 560, 120, 36), "CLOSE", self._toggle_how_to_play, color=(60, 65, 75))

    def _toggle_how_to_play(self) -> None:
        self.show_how_to_play = not self.show_how_to_play

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.show_how_to_play:
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                self.show_how_to_play = False
            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                self.how_to_play_tab = int(event.unicode)
            self.btn_close_help.handle_event(event)
            return

        self.btn_start.handle_event(event)
        self.btn_how_to_play.handle_event(event)
        self.btn_quit.handle_event(event)

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(COLOR_BG)

        # Subtle paper grid pattern in background
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(surface, (45, 48, 56), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(surface, (45, 48, 56), (0, y), (SCREEN_WIDTH, y), 1)

        # Title
        FontManager.render_text(surface, "PAPER WARFIRE", SCREEN_WIDTH // 2, 180, size=46, color=COLOR_TEXT, center=True)
        FontManager.render_text(surface, "SIMULTANEOUS TURN-BASED GRID STRATEGY", SCREEN_WIDTH // 2, 230, size=16, color=COLOR_ACCENT, center=True)
        FontManager.render_text(surface, "Spec-Driven Development Architecture (Phase 2)", SCREEN_WIDTH // 2, 255, size=13, color=COLOR_TEXT_DIM, center=True)

        # Main Navigation Buttons
        self.btn_start.render(surface)
        self.btn_how_to_play.render(surface)
        self.btn_quit.render(surface)

        # Footer credit
        FontManager.render_text(surface, "Based on original paper war concept by @datureksa0045", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 35, size=12, color=COLOR_TEXT_DIM, center=True)

        # Overlay Modal for How to Play
        if self.show_how_to_play:
            self._render_how_to_play(surface)

    def _render_how_to_play(self, surface: pygame.Surface) -> None:
        dim = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 190))
        surface.blit(dim, (0, 0))

        mw, mh = 760, 480
        mx, my = (SCREEN_WIDTH - mw) // 2, (SCREEN_HEIGHT - mh) // 2 - 20
        modal_rect = pygame.Rect(mx, my, mw, mh)
        pygame.draw.rect(surface, COLOR_PANEL_BG, modal_rect, border_radius=6)
        pygame.draw.rect(surface, COLOR_PANEL_BORDER, modal_rect, 2, border_radius=6)

        FontManager.render_text(surface, "HOW TO PLAY - TACTICAL MANUAL", SCREEN_WIDTH // 2, my + 30, size=22, color=COLOR_ACCENT, center=True)

        # Tabs hint
        tab_hint = f"Tab {self.how_to_play_tab}/3 (Press 1, 2, or 3 to switch)"
        FontManager.render_text(surface, tab_hint, SCREEN_WIDTH // 2, my + 58, size=13, color=COLOR_TEXT_DIM, center=True)

        content_y = my + 95
        if self.how_to_play_tab == 1:
            FontManager.render_text(surface, "1. THE WEGO CYCLE (SIMULTANEOUS ORDERS)", mx + 40, content_y, size=16, color=COLOR_TEXT)
            lines = [
                "• Planning Phase: You and the AI plan 1 action (MOVE or ATTACK) per unit.",
                "• No actions happen immediately during planning. All orders remain hidden!",
                "• War Phase: Press READY to simultaneously execute all orders across both armies:",
                "   1. Movement: Units advance together. If two clash at the same tile, both bounce back!",
                "   2. Recon: Vision is updated based on new unit positions.",
                "   3. Firing: Attacks land simultaneously with full AoE falloff calculations.",
                "   4. Casualties: Destroyed units are removed, granting tactical bounty coins."
            ]
            for i, line in enumerate(lines):
                FontManager.render_text(surface, line, mx + 40, content_y + 30 + i * 24, size=13, color=COLOR_TEXT_DIM)

        elif self.how_to_play_tab == 2:
            FontManager.render_text(surface, "2. FOG OF WAR & COORDINATE TARGETING", mx + 40, content_y, size=16, color=COLOR_TEXT)
            lines = [
                "• Unexplored Fog (Pitch Black): Unknown terrain and hidden enemy units.",
                "• Explored / Shrouded: Terrain layout is remembered, but hidden enemies are invisible.",
                "• Visible: Tiles actively illuminated by your living units or recent explosions.",
                "• Manual Coordinate Bombardment:",
                "   - Type target coordinates directly into the panel (e.g. 'H8' or '14, 8').",
                "   - Blind Firing: You can fire into black fog to guess enemy positions!",
                "   - Artillery, Tank, and Mortar attacks explode in a 3x3 AoE, revealing fog."
            ]
            for i, line in enumerate(lines):
                FontManager.render_text(surface, line, mx + 40, content_y + 30 + i * 24, size=13, color=COLOR_TEXT_DIM)

        else:
            FontManager.render_text(surface, "3. SQUAD UNITS & VICTORY OBJECTIVES", mx + 40, content_y, size=16, color=COLOR_TEXT)
            lines = [
                "• Pistol: Fast 4-tile scout, rapid reaction single-target fire.",
                "• Machine Gun: 3-tile move, 3x3 area suppression fire to disrupt formations.",
                "• Sniper: Long range 12-tile precision fire, high single-target burst damage.",
                "• Tank: 200 HP heavy armor vanguard, absorbs hits with 3x3 cannon blasts.",
                "• Mortar & Artillery: Mid and extreme range siege bombardment.",
                "• Objective: Eliminate all enemy units to achieve VICTORY!",
                "• Defeat: Occurs if all your units are destroyed or the 25-turn limit expires."
            ]
            for i, line in enumerate(lines):
                FontManager.render_text(surface, line, mx + 40, content_y + 30 + i * 24, size=13, color=COLOR_TEXT_DIM)

        self.btn_close_help.render(surface)


class PauseModal:
    def __init__(self, on_resume: Callable, on_restart: Callable, on_menu: Callable):
        self.on_resume = on_resume
        self.on_restart = on_restart
        self.on_menu = on_menu

        btn_w, btn_h = 220, 40
        cx = SCREEN_WIDTH // 2 - btn_w // 2
        cy = SCREEN_HEIGHT // 2 - 60

        self.btn_resume = Button(pygame.Rect(cx, cy, btn_w, btn_h), "RESUME MATCH", self.on_resume, color=(40, 110, 60))
        self.btn_restart = Button(pygame.Rect(cx, cy + 55, btn_w, btn_h), "RESTART BATTLE", self.on_restart, color=(100, 80, 40))
        self.btn_menu = Button(pygame.Rect(cx, cy + 110, btn_w, btn_h), "RETURN TO MENU", self.on_menu, color=(90, 40, 40))

    def handle_event(self, event: pygame.event.Event) -> None:
        self.btn_resume.handle_event(event)
        self.btn_restart.handle_event(event)
        self.btn_menu.handle_event(event)

    def render(self, surface: pygame.Surface) -> None:
        dim = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 180))
        surface.blit(dim, (0, 0))

        mw, mh = 360, 260
        mx, my = (SCREEN_WIDTH - mw) // 2, (SCREEN_HEIGHT - mh) // 2
        modal_rect = pygame.Rect(mx, my, mw, mh)
        pygame.draw.rect(surface, COLOR_PANEL_BG, modal_rect, border_radius=6)
        pygame.draw.rect(surface, COLOR_PANEL_BORDER, modal_rect, 2, border_radius=6)

        FontManager.render_text(surface, "MATCH PAUSED", SCREEN_WIDTH // 2, my + 30, size=22, color=COLOR_ACCENT, center=True)

        self.btn_resume.render(surface)
        self.btn_restart.render(surface)
        self.btn_menu.render(surface)

