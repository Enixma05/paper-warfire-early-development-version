"""Input Handler for Paper Warfire.
Maps screen mouse clicks to grid tiles, handles WASD camera panning,
and captures keyboard input for targeting.
"""

from typing import Tuple, Optional
import pygame

from src.core.constants import (
    GRID_COLS, GRID_ROWS, TILE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y
)

class InputHandler:
    def __init__(self):
        self.camera_x = 0
        self.camera_y = 0
        self.pan_speed = 300  # pixels per second

    def screen_to_grid(self, screen_x: int, screen_y: int) -> Optional[Tuple[int, int]]:
        """Converts window pixel coordinates into grid (col, row) coordinates."""
        rel_x = screen_x - GRID_OFFSET_X - self.camera_x
        rel_y = screen_y - GRID_OFFSET_Y - self.camera_y

        if rel_x < 0 or rel_y < 0:
            return None

        gx = rel_x // TILE_SIZE
        gy = rel_y // TILE_SIZE

        if 0 <= gx < GRID_COLS and 0 <= gy < GRID_ROWS:
            return (gx, gy)

        return None

    def grid_to_screen(self, gx: int, gy: int) -> Tuple[int, int]:
        """Converts grid (col, row) to top-left pixel coordinate on screen."""
        sx = GRID_OFFSET_X + self.camera_x + gx * TILE_SIZE
        sy = GRID_OFFSET_Y + self.camera_y + gy * TILE_SIZE
        return (sx, sy)

    def update_camera(self, dt: float, disable_wasd: bool = False) -> None:
        """Pans camera when arrow keys or WASD are held down.
        If disable_wasd is True (e.g. typing in text box), WASD keys will not pan the camera.
        """
        keys = pygame.key.get_pressed()
        step = int(self.pan_speed * dt)
        allow_wasd = not disable_wasd

        if (allow_wasd and keys[pygame.K_a]) or keys[pygame.K_LEFT]:
            self.camera_x = min(100, self.camera_x + step)
        if (allow_wasd and keys[pygame.K_d]) or keys[pygame.K_RIGHT]:
            self.camera_x = max(-200, self.camera_x - step)
        if (allow_wasd and keys[pygame.K_w]) or keys[pygame.K_UP]:
            self.camera_y = min(100, self.camera_y + step)
        if (allow_wasd and keys[pygame.K_s]) or keys[pygame.K_DOWN]:
            self.camera_y = max(-150, self.camera_y - step)

    def reset_camera(self) -> None:
        self.camera_x = 0
        self.camera_y = 0

