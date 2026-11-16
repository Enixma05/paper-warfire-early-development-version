"""PlayerUnit: Subclass of BaseUnit representing friendly playable forces.
"""

from typing import Optional
from src.core.constants import Team
from src.game.config import UnitType, UnitStats
from src.game.base_unit import BaseUnit

class PlayerUnit(BaseUnit):
    def __init__(
        self,
        unit_id: str,
        unit_type: UnitType,
        x: int,
        y: int,
        custom_stats: Optional[UnitStats] = None
    ):
        super().__init__(
            unit_id=unit_id,
            unit_type=unit_type,
            team=Team.PLAYER,
            x=x,
            y=y,
            custom_stats=custom_stats
        )

