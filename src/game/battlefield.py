"""Battlefield Grid Manager for Paper Warfire.
Handles 24x16 tile matrix, procedural terrain generation, coordinate parsing,
and BFS reachable tiles pathfinding.
"""

import random
from typing import List, Tuple, Optional, Dict, Set
from collections import deque

from src.core.constants import GRID_COLS, GRID_ROWS
from src.game.config import TerrainType, TerrainStats, DEFAULT_TERRAIN_STATS
from src.game.base_unit import BaseUnit

class Tile:
    def __init__(self, x: int, y: int, terrain_type: TerrainType = TerrainType.PLAINS):
        self.x = x
        self.y = y
        self.terrain_type = terrain_type
        self.occupant: Optional[BaseUnit] = None

    @property
    def stats(self) -> TerrainStats:
        return DEFAULT_TERRAIN_STATS[self.terrain_type]

    def __repr__(self) -> str:
        occ = f"[{self.occupant.unit_id}]" if self.occupant else "[ ]"
        return f"Tile({self.x},{self.y} {self.terrain_type.name} {occ})"


class Battlefield:
    def __init__(self, cols: int = GRID_COLS, rows: int = GRID_ROWS, seed: Optional[int] = None):
        self.cols = cols
        self.rows = rows
        self.grid: List[List[Tile]] = [
            [Tile(x, y) for y in range(rows)] for x in range(cols)
        ]
        self.units: List[BaseUnit] = []
        self.generate_terrain(seed)

    def generate_terrain(self, seed: Optional[int] = None) -> None:
        """
        Generates tactical terrain:
        - Cols 0-3: Player initial zone (Clear plains, few cover trees)
        - Cols 4-19: Neutral zone (Strategic choke point mountains, forest cover, swamps)
        - Cols 20-23: Enemy initial zone (Clear plains, few cover trees)
        """
        rng = random.Random(seed) if seed is not None else random.Random()

        for x in range(self.cols):
            for y in range(self.rows):
                if x < 4 or x >= self.cols - 4:
                    # Spawn zones
                    roll = rng.random()
                    if roll < 0.15:
                        t = TerrainType.FOREST
                    else:
                        t = TerrainType.PLAINS
                else:
                    # Contested central battlefield
                    roll = rng.random()
                    if roll < 0.10:
                        t = TerrainType.MOUNTAIN
                    elif roll < 0.30:
                        t = TerrainType.FOREST
                    elif roll < 0.42:
                        t = TerrainType.WATER
                    else:
                        t = TerrainType.PLAINS

                self.grid[x][y].terrain_type = t
                self.grid[x][y].occupant = None

    def is_valid_coord(self, x: int, y: int) -> bool:
        return 0 <= x < self.cols and 0 <= y < self.rows

    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        if self.is_valid_coord(x, y):
            return self.grid[x][y]
        return None

    def get_unit_at(self, x: int, y: int) -> Optional[BaseUnit]:
        tile = self.get_tile(x, y)
        return tile.occupant if tile else None

    def place_unit(self, unit: BaseUnit, x: int, y: int) -> bool:
        """Places a unit at (x, y) validating footprint bounds and passability."""
        # Check all footprint tiles
        for dx in range(unit.width):
            for dy in range(unit.height):
                tx, ty = x + dx, y + dy
                tile = self.get_tile(tx, ty)
                if not tile or not tile.stats.is_passable:
                    return False
                if tile.occupant is not None and tile.occupant != unit:
                    return False

        # Clear old footprint if already on grid
        self.remove_unit_from_tiles(unit)

        # Place on new footprint
        unit.x = x
        unit.y = y
        for dx in range(unit.width):
            for dy in range(unit.height):
                self.grid[x + dx][y + dy].occupant = unit

        if unit not in self.units:
            self.units.append(unit)
        return True

    def remove_unit_from_tiles(self, unit: BaseUnit) -> None:
        """Removes the unit's reference from grid tiles without deleting the unit from the unit list."""
        for x in range(self.cols):
            for y in range(self.rows):
                if self.grid[x][y].occupant == unit:
                    self.grid[x][y].occupant = None

    def remove_unit(self, unit: BaseUnit) -> None:
        """Removes a destroyed unit completely from the battlefield."""
        self.remove_unit_from_tiles(unit)
        if unit in self.units:
            self.units.remove(unit)

    def can_unit_occupy(self, unit: BaseUnit, x: int, y: int) -> bool:
        """Verifies if the unit's entire footprint can fit at (x, y)."""
        for dx in range(unit.width):
            for dy in range(unit.height):
                tx, ty = x + dx, y + dy
                tile = self.get_tile(tx, ty)
                if not tile or not tile.stats.is_passable:
                    return False
                if tile.occupant is not None and tile.occupant != unit:
                    return False
        return True

    def get_reachable_tiles(self, unit: BaseUnit) -> List[Tuple[int, int]]:
        """
        Uses Breadth-First Search (Dijkstra-like BFS) with terrain movement cost
        to calculate all valid destination tiles (top-left of footprint) reachable within unit.move_range.
        """
        if not unit.is_alive:
            return []

        start = (unit.x, unit.y)
        reachable: Dict[Tuple[int, int], float] = {start: 0.0}
        queue = deque([(start, 0.0)])

        while queue:
            (curr_x, curr_y), curr_cost = queue.popleft()

            # Orthogonal 4-directional movement
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = curr_x + dx, curr_y + dy

                if not self.can_unit_occupy(unit, nx, ny):
                    continue

                # Movement cost is determined by destination terrain
                step_cost = self.grid[nx][ny].stats.move_cost
                new_cost = curr_cost + step_cost

                if new_cost <= unit.move_range:
                    if (nx, ny) not in reachable or new_cost < reachable[(nx, ny)]:
                        reachable[(nx, ny)] = new_cost
                        queue.append(((nx, ny), new_cost))

        return list(reachable.keys())

    @staticmethod
    def parse_coordinate(input_str: str) -> Optional[Tuple[int, int]]:
        """
        Parses coordinates from either:
        - Alphanumeric notation like 'H8', 'A1', 'X16'
        - Numeric notation like '14, 8', '14 8', 'X: 14, Y: 8'
        Returns (x, y) 0-indexed tuple, or None if invalid.
        """
        cleaned = input_str.strip().upper().replace("X:", "").replace("Y:", "").replace("(", "").replace(")", "")

        # Try comma or whitespace separated integers first
        for sep in [",", " "]:
            if sep in cleaned:
                parts = [p.strip() for p in cleaned.split(sep) if p.strip()]
                if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                    x = int(parts[0])
                    y = int(parts[1])
                    if 0 <= x < GRID_COLS and 0 <= y < GRID_ROWS:
                        return (x, y)

        # Try alphanumeric like 'H8' or 'X16'
        # First char is column A-X -> 0-23
        if len(cleaned) >= 2 and cleaned[0].isalpha():
            col_char = cleaned[0]
            col = ord(col_char) - ord('A')
            row_part = cleaned[1:]
            if row_part.isdigit():
                row = int(row_part) - 1  # 1-indexed to 0-indexed
                if 0 <= col < GRID_COLS and 0 <= row < GRID_ROWS:
                    return (col, row)

        return None

    @staticmethod
    def format_coordinate(x: int, y: int) -> str:
        """Formats 0-indexed (x, y) to alphanumeric string like 'H8' (Col H, Row 8)."""
        col_char = chr(ord('A') + x)
        row_num = y + 1
        return f"{col_char}{row_num}"

