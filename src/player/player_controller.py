"""Player Controller for Paper Warfire.
Manages unit selection, manual coordinate input, command queue assignment,
wallet economy, and upgrade purchasing.
"""

from typing import List, Tuple, Optional, Dict
from src.core.constants import Team
from src.game.config import UpgradeItem, DEFAULT_UPGRADES, EconomyConfig
from src.game.command import Command, CommandType
from src.game.base_unit import BaseUnit
from src.player.player_unit import PlayerUnit
from src.game.battlefield import Battlefield
from src.game.fog_of_war import FogOfWarManager

class PlayerController:
    def __init__(self, battlefield: Battlefield, fow_manager: FogOfWarManager, starting_coins: int = 100):
        self.battlefield = battlefield
        self.fow = fow_manager
        self.coins = starting_coins
        self.selected_unit: Optional[PlayerUnit] = None
        self.econ = EconomyConfig()
        self.is_ready = False

    def select_unit_at(self, x: int, y: int) -> Optional[PlayerUnit]:
        occupant = self.battlefield.get_unit_at(x, y)
        if occupant and occupant.team == Team.PLAYER and occupant.is_alive:
            self.selected_unit = occupant  # type: ignore
            return self.selected_unit
        return None

    def deselect(self) -> None:
        self.selected_unit = None

    def assign_move_command(self, target_coord: Tuple[int, int]) -> Tuple[bool, str]:
        if not self.selected_unit:
            return False, "No unit selected."

        reachable = self.battlefield.get_reachable_tiles(self.selected_unit)
        if target_coord not in reachable:
            return False, f"Coordinate {target_coord} is unreachable."

        cmd = Command(
            unit_id=self.selected_unit.unit_id,
            command_type=CommandType.MOVE,
            target_coord=target_coord
        )
        self.selected_unit.assign_command(cmd)
        return True, f"Move order assigned to {target_coord}."

    def assign_attack_command(self, target_coord: Tuple[int, int]) -> Tuple[bool, str]:
        if not self.selected_unit:
            return False, "No unit selected."

        tx, ty = target_coord
        if not self.battlefield.is_valid_coord(tx, ty):
            return False, f"Coordinate {target_coord} is out of battlefield bounds."

        # Range check
        dist = max(abs(self.selected_unit.x - tx), abs(self.selected_unit.y - ty))
        max_range = self.selected_unit.get_effective_attack_range()
        if dist > max_range:
            return False, f"Target out of range! Distance {dist} > Max {max_range}."

        cmd = Command(
            unit_id=self.selected_unit.unit_id,
            command_type=CommandType.ATTACK,
            target_coord=target_coord
        )
        self.selected_unit.assign_command(cmd)
        return True, f"Attack order assigned to {target_coord}."

    def cancel_unit_command(self, unit: PlayerUnit) -> None:
        unit.clear_command()

    def clear_all_commands(self) -> None:
        for u in self.get_player_units():
            u.clear_command()
        self.is_ready = False

    def get_player_units(self) -> List[PlayerUnit]:
        return [u for u in self.battlefield.units if u.team == Team.PLAYER and u.is_alive]  # type: ignore

    def get_command_queue(self) -> List[Tuple[PlayerUnit, Command]]:
        queue = []
        for u in self.get_player_units():
            if u.planned_command:
                queue.append((u, u.planned_command))
        return queue

    def add_coins(self, amount: int) -> None:
        self.coins += max(0, amount)

    def buy_upgrade(self, unit: PlayerUnit, upgrade_id: str) -> Tuple[bool, str]:
        if upgrade_id not in DEFAULT_UPGRADES:
            return False, "Unknown upgrade."

        item = DEFAULT_UPGRADES[upgrade_id]
        if self.coins < item.cost:
            return False, f"Not enough coins. Need {item.cost}, have {self.coins}."

        if upgrade_id in unit.upgrades:
            return False, f"Unit already has {item.name}."

        self.coins -= item.cost
        unit.apply_upgrade(item)
        return True, f"Purchased {item.name} for {unit.unit_type.value}."

    def use_scan_drone(self, target_coord: Tuple[int, int]) -> Tuple[bool, str]:
        item = DEFAULT_UPGRADES["scan_drone"]
        if self.coins < item.cost:
            return False, f"Not enough coins for Scan Drone ({item.cost} required)."

        tx, ty = target_coord
        if not self.battlefield.is_valid_coord(tx, ty):
            return False, "Invalid coordinate."

        self.coins -= item.cost
        self.fow.reveal_area(tx, ty, radius=2)  # 5x5 reveal
        return True, f"Scan Drone deployed at {target_coord}! Area revealed."
