"""Fog of War Manager for Paper Warfire.
Tracks visibility states (UNEXPLORED, EXPLORED, VISIBLE), handles dynamic sight updates,
and processes impact/scan reveals.
"""

from typing import List, Tuple, Set, Dict, Optional
from src.core.constants import GRID_COLS, GRID_ROWS, Visibility, Team
from src.game.base_unit import BaseUnit

class FogOfWarManager:
    def __init__(self, cols: int = GRID_COLS, rows: int = GRID_ROWS, team: Team = Team.PLAYER):
        self.cols = cols
        self.rows = rows
        self.team = team
        # 2D grid storing Visibility enum
        self.visibility: List[List[Visibility]] = [
            [Visibility.UNEXPLORED for _ in range(rows)] for _ in range(cols)
        ]
        self.temporary_reveals: Set[Tuple[int, int]] = set()

    def is_visible(self, x: int, y: int) -> bool:
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return self.visibility[x][y] == Visibility.VISIBLE
        return False

    def is_explored(self, x: int, y: int) -> bool:
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return self.visibility[x][y] in (Visibility.EXPLORED, Visibility.VISIBLE)
        return False

    def get_visibility(self, x: int, y: int) -> Visibility:
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return self.visibility[x][y]
        return Visibility.UNEXPLORED

    def update_visibility(self, units: List[BaseUnit]) -> int:
        """
        Updates vision based on all living units belonging to this team.
        Tiles currently in range -> VISIBLE.
        Tiles previously seen that are now out of range -> EXPLORED.
        Returns the number of newly discovered tiles (for coin reward).
        """
        new_visible: Set[Tuple[int, int]] = set()
        friendly_units = [u for u in units if u.team == self.team and u.is_alive]

        for unit in friendly_units:
            sight = unit.get_effective_sight_range()
            # Check bounding box around unit footprint
            min_x = max(0, unit.x - sight)
            max_x = min(self.cols - 1, unit.x + unit.width - 1 + sight)
            min_y = max(0, unit.y - sight)
            max_y = min(self.rows - 1, unit.y + unit.height - 1 + sight)

            for tx in range(min_x, max_x + 1):
                for ty in range(min_y, max_y + 1):
                    # Chebyshev distance from unit footprint
                    dx = max(0, unit.x - tx, tx - (unit.x + unit.width - 1))
                    dy = max(0, unit.y - ty, ty - (unit.y + unit.height - 1))
                    dist = max(dx, dy)
                    if dist <= sight:
                        new_visible.add((tx, ty))

        # Add temporary reveals (impact reveals / drone scans)
        for rx, ry in self.temporary_reveals:
            if 0 <= rx < self.cols and 0 <= ry < self.rows:
                new_visible.add((rx, ry))

        newly_discovered_count = 0

        for x in range(self.cols):
            for y in range(self.rows):
                curr = self.visibility[x][y]
                if (x, y) in new_visible:
                    if curr == Visibility.UNEXPLORED:
                        newly_discovered_count += 1
                    self.visibility[x][y] = Visibility.VISIBLE
                else:
                    if curr == Visibility.VISIBLE:
                        self.visibility[x][y] = Visibility.EXPLORED

        return newly_discovered_count

    def reveal_area(self, center_x: int, center_y: int, radius: int = 1) -> None:
        """Reveals an area (e.g. 3x3 for radius=1, 5x5 for radius=2) temporarily."""
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                tx, ty = center_x + dx, center_y + dy
                if 0 <= tx < self.cols and 0 <= ty < self.rows:
                    self.temporary_reveals.add((tx, ty))
                    self.visibility[tx][ty] = Visibility.VISIBLE

    def clear_temporary_reveals(self) -> None:
        self.temporary_reveals.clear()

    def get_explored_ratio(self) -> float:
        """Returns percentage of explored/visible tiles on map (0.0 to 1.0)."""
        total = self.cols * self.rows
        explored = sum(
            1 for x in range(self.cols) for y in range(self.rows)
            if self.visibility[x][y] != Visibility.UNEXPLORED
        )
        return explored / max(1, total)

