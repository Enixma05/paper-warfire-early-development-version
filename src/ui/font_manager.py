"""Font Manager and Geometric Vector Sprite Renderer for Paper Warfire.
Provides clean typography, procedural minimalist vector drawings, and seamless
support for manual custom sprites (PNG) when added to assets/sprites/.
"""

import os
from typing import Tuple, Optional, Dict
import pygame

from src.core.constants import (
    COLOR_PLAYER, COLOR_ENEMY, COLOR_ACCENT, COLOR_TEXT, COLOR_TEXT_DIM,
    Team, TILE_SIZE
)
from src.game.config import UnitType
from src.game.base_unit import BaseUnit

class FontManager:
    _fonts: Dict[int, pygame.font.Font] = {}

    @classmethod
    def get_font(cls, size: int) -> pygame.font.Font:
        if size not in cls._fonts:
            # Check if custom font exists in assets/fonts/
            custom_font_dir = os.path.join("assets", "fonts")
            loaded = False
            if os.path.exists(custom_font_dir):
                for f in os.listdir(custom_font_dir):
                    if f.lower().endswith(".ttf") or f.lower().endswith(".otf"):
                        try:
                            cls._fonts[size] = pygame.font.Font(os.path.join(custom_font_dir, f), size)
                            loaded = True
                            break
                        except Exception:
                            pass
            if not loaded:
                try:
                    cls._fonts[size] = pygame.font.SysFont("Consolas, Courier, monospace", size)
                except Exception:
                    cls._fonts[size] = pygame.font.Font(None, size)
        return cls._fonts[size]

    @classmethod
    def render_text(
        cls,
        surface: pygame.Surface,
        text: str,
        x: int,
        y: int,
        size: int = 16,
        color: Tuple[int, int, int] = COLOR_TEXT,
        center: bool = False
    ) -> pygame.Rect:
        font = cls.get_font(size)
        rendered = font.render(text, True, color)
        rect = rendered.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        surface.blit(rendered, rect)
        return rect


class VectorUnitRenderer:
    """
    Renders unit visual representations.
    Supports seamless fallback:
    1. If a custom sprite PNG exists in assets/sprites/ (e.g. pistol.png, tank.png), blit it.
    2. Otherwise, procedurally render the geometric minimalist vector insignia.
    """
    _sprite_cache: Dict[Tuple[UnitType, int, int], Optional[pygame.Surface]] = {}

    @classmethod
    def _get_custom_sprite(cls, unit_type: UnitType, width: int, height: int) -> Optional[pygame.Surface]:
        key = (unit_type, width, height)
        if key in cls._sprite_cache:
            return cls._sprite_cache[key]

        slug = unit_type.name.lower().replace(" ", "_")
        val_slug = unit_type.value.lower().replace(" ", "_")
        candidates = [
            os.path.join("assets", "sprites", f"{slug}.png"),
            os.path.join("assets", "sprites", f"{val_slug}.png"),
            os.path.join("assets", "sprites", f"{unit_type.name.lower()}.png"),
        ]

        for path in candidates:
            if os.path.exists(path):
                try:
                    img = pygame.image.load(path).convert_alpha()
                    scaled = pygame.transform.scale(img, (width, height))
                    cls._sprite_cache[key] = scaled
                    return scaled
                except Exception:
                    pass

        cls._sprite_cache[key] = None
        return None

    @classmethod
    def draw_unit(
        cls,
        surface: pygame.Surface,
        unit: BaseUnit,
        screen_x: int,
        screen_y: int,
        is_selected: bool = False
    ) -> None:
        color = COLOR_PLAYER if unit.team == Team.PLAYER else COLOR_ENEMY
        w = unit.width * TILE_SIZE
        h = unit.height * TILE_SIZE
        pad = 3
        inner_w = w - pad * 2
        inner_h = h - pad * 2

        # Outer unit body container
        body_rect = pygame.Rect(screen_x + pad, screen_y + pad, inner_w, inner_h)
        pygame.draw.rect(surface, (20, 22, 28), body_rect)

        # Check for custom sprite
        sprite = cls._get_custom_sprite(unit.unit_type, inner_w, inner_h)
        if sprite:
            surface.blit(sprite, (screen_x + pad, screen_y + pad))
        else:
            # Procedural Geometric Minimalist Vector Drawing
            cx, cy = body_rect.centerx, body_rect.centery

            if unit.unit_type == UnitType.PISTOL:
                # Single tactical chevron pointing forward
                pygame.draw.polygon(surface, color, [(cx - 6, cy + 6), (cx, cy - 6), (cx + 6, cy + 6)], 2)
            elif unit.unit_type == UnitType.MACHINE_GUN:
                # Dual suppressive bars
                pygame.draw.line(surface, color, (cx - 7, cy - 4), (cx + 7, cy - 4), 3)
                pygame.draw.line(surface, color, (cx - 7, cy + 4), (cx + 7, cy + 4), 3)
            elif unit.unit_type == UnitType.SNIPER:
                # Crosshair circle & dot
                pygame.draw.circle(surface, color, (cx, cy), 7, 2)
                pygame.draw.circle(surface, color, (cx, cy), 2)
            elif unit.unit_type == UnitType.TANK:
                # Heavy armored chassis & turret cannon
                pygame.draw.rect(surface, color, (cx - 14, cy - 10, 28, 20), 2)
                pygame.draw.circle(surface, color, (cx, cy), 8)
                pygame.draw.line(surface, color, (cx, cy), (cx + 14, cy), 3)
            elif unit.unit_type == UnitType.MORTAR:
                # Parabolic launcher tube
                pygame.draw.circle(surface, color, (cx - 4, cy + 4), 4)
                pygame.draw.line(surface, color, (cx - 4, cy + 4), (cx + 8, cy - 8), 3)
            elif unit.unit_type == UnitType.ARTILLERY:
                # Long heavy siege cannon
                pygame.draw.rect(surface, color, (cx - 10, cy - 6, 20, 12), 2)
                pygame.draw.line(surface, color, (cx, cy), (cx + 18, cy), 4)

        # Team / Selection Border
        border_width = 3 if is_selected else 2
        border_color = COLOR_ACCENT if is_selected else color
        pygame.draw.rect(surface, border_color, body_rect, border_width)

        # Draw Health Bar on top
        hp_ratio = unit.current_hp / max(1, unit.max_hp)
        bar_w = w - pad * 2 - 4
        bar_h = 4
        bar_x = screen_x + pad + 2
        bar_y = screen_y + pad + 2

        pygame.draw.rect(surface, (10, 10, 12), (bar_x, bar_y, bar_w, bar_h))

        if hp_ratio > 0.5:
            hp_color = (60, 180, 80)
        elif hp_ratio > 0.25:
            hp_color = (230, 190, 40)
        else:
            hp_color = (220, 50, 50)

        pygame.draw.rect(surface, hp_color, (bar_x, bar_y, int(bar_w * hp_ratio), bar_h))
