"""Coordinate Text Input Component for Paper Warfire.
Allows players to manually type target coordinates (e.g. 'H8' or '14, 8'),
providing real-time feedback and validation.
"""

from typing import Tuple, Optional
import pygame

from src.core.constants import COLOR_TEXT, COLOR_TEXT_DIM, COLOR_ACCENT
from src.game.battlefield import Battlefield
from src.ui.font_manager import FontManager

class CoordinateInputBox:
    def __init__(self, x: int, y: int, width: int = 140, height: int = 32):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.is_active = False
        self.parsed_coord: Optional[Tuple[int, int]] = None
        self.error_message: str = ""

    def handle_event(self, event: pygame.event.Event) -> Optional[Tuple[int, int]]:
        """
        Handles clicks to focus/unfocus and keyboard typing.
        Returns confirmed (x, y) if user pressed ENTER on a valid coordinate.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_active = True
            else:
                self.is_active = False

        elif event.type == pygame.KEYDOWN and self.is_active:
            if event.key == pygame.K_RETURN:
                if self.parsed_coord is not None:
                    confirmed = self.parsed_coord
                    return confirmed
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self._validate()
            elif event.key == pygame.K_ESCAPE:
                self.is_active = False
            else:
                # Accept letters, numbers, comma, colon, space
                if len(self.text) < 10 and (event.unicode.isalnum() or event.unicode in (",", " ", ":")):
                    self.text += event.unicode
                    self._validate()

        return None

    def set_coordinate(self, coord: Tuple[int, int]) -> None:
        self.text = Battlefield.format_coordinate(coord[0], coord[1])
        self._validate()

    def clear(self) -> None:
        self.text = ""
        self.parsed_coord = None
        self.error_message = ""

    def _validate(self) -> None:
        if not self.text.strip():
            self.parsed_coord = None
            self.error_message = ""
            return

        parsed = Battlefield.parse_coordinate(self.text)
        if parsed is not None:
            self.parsed_coord = parsed
            self.error_message = ""
        else:
            self.parsed_coord = None
            self.error_message = "Gunakan format H8 atau X,Y (1-24, 1-16)"

    def render(self, surface: pygame.Surface) -> None:
        # Border color based on validation state
        if self.parsed_coord is not None:
            border_color = (60, 180, 80)   # Green valid
        elif self.error_message:
            border_color = (220, 60, 60)   # Red invalid
        elif self.is_active:
            border_color = COLOR_ACCENT    # Gold focused
        else:
            border_color = (80, 85, 95)    # Neutral dim

        # Background box
        pygame.draw.rect(surface, (20, 22, 28), self.rect)
        pygame.draw.rect(surface, border_color, self.rect, 2)

        # Text display
        display_str = self.text if self.text else "H8 / X,Y..."
        text_color = COLOR_TEXT if self.text else COLOR_TEXT_DIM
        FontManager.render_text(
            surface,
            display_str,
            self.rect.x + 8,
            self.rect.y + 7,
            size=14,
            color=text_color
        )

        # Error / helper hint
        if self.error_message:
            FontManager.render_text(
                surface,
                self.error_message,
                self.rect.x,
                self.rect.bottom + 4,
                size=11,
                color=(240, 80, 80)
            )
        elif self.parsed_coord:
            coord_str = f"Target: ({self.parsed_coord[0]}, {self.parsed_coord[1]}) | {Battlefield.format_coordinate(self.parsed_coord[0], self.parsed_coord[1])}"
            FontManager.render_text(
                surface,
                coord_str,
                self.rect.x,
                self.rect.bottom + 4,
                size=11,
                color=(100, 200, 120)
            )

