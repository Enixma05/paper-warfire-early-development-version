"""EnemyUnit: Subclass of BaseUnit representing opponent AI forces.
Includes threat score and AI priority parameters.
"""

from typing import Optional
from src.core.constants import Team
from src.game.config import UnitType, UnitStats
from src.game.base_unit import BaseUnit

class EnemyUnit(BaseUnit):
    def __init__(
        self,
        unit_id: str,
        unit_type: UnitType,
        x: int,
        y: int,
        custom_stats: Optional[UnitStats] = None,
        ai_priority_weight: int = 10
    ):
        super().__init__(
            unit_id=unit_id,
            unit_type=unit_type,
            team=Team.ENEMY,
            x=x,
            y=y,
            custom_stats=custom_stats
        )
        self.ai_priority_weight = ai_priority_weight

    def get_threat_score(self) -> float:
        """Evaluates tactical threat based on base damage, range, and current HP."""
        if not self.is_alive:
            return 0.0
        hp_ratio = self.current_hp / max(1, self.max_hp)
        return (self.stats.base_damage * 1.5 + self.stats.attack_range) * hp_ratio

