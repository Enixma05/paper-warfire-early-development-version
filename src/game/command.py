"""Command data structures for simultaneous WEGO execution.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Tuple, Optional

class CommandType(Enum):
    MOVE = auto()
    ATTACK = auto()
    SCAN = auto()
    IDLE = auto()


@dataclass
class Command:
    unit_id: str
    command_type: CommandType
    target_coord: Tuple[int, int]  # (grid_x, grid_y)
    is_valid: bool = True
    status_message: str = ""

    def __repr__(self) -> str:
        return f"Command({self.command_type.name} unit={self.unit_id} to={self.target_coord})"

