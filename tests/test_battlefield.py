import pytest
from src.game.battlefield import Battlefield
from src.game.config import UnitType, TerrainType
from src.game.base_unit import BaseUnit
from src.core.constants import Team

def test_battlefield_initialization():
    bf = Battlefield(cols=24, rows=16, seed=42)
    assert bf.cols == 24
    assert bf.rows == 16
    assert bf.get_tile(0, 0) is not None
    assert bf.get_tile(25, 20) is None

def test_coordinate_parsing():
    # Numeric
    assert Battlefield.parse_coordinate("14, 8") == (14, 8)
    assert Battlefield.parse_coordinate("X: 14, Y: 8") == (14, 8)
    assert Battlefield.parse_coordinate("0, 0") == (0, 0)
    
    # Alphanumeric
    # A1 -> (0, 0)
    assert Battlefield.parse_coordinate("A1") == (0, 0)
    # H8 -> (7, 7)
    assert Battlefield.parse_coordinate("H8") == (7, 7)
    # X16 -> (23, 15)
    assert Battlefield.parse_coordinate("X16") == (23, 15)
    
    # Invalid
    assert Battlefield.parse_coordinate("Z99") is None
    assert Battlefield.parse_coordinate("invalid") is None

def test_coordinate_formatting():
    assert Battlefield.format_coordinate(0, 0) == "A1"
    assert Battlefield.format_coordinate(7, 7) == "H8"
    assert Battlefield.format_coordinate(23, 15) == "X16"

def test_unit_placement_and_footprint():
    bf = Battlefield(cols=24, rows=16, seed=42)
    # Pistol footprint 1x1
    pistol = BaseUnit("p1", UnitType.PISTOL, Team.PLAYER, 0, 0)
    assert bf.place_unit(pistol, 2, 2) is True
    assert bf.get_unit_at(2, 2) == pistol
    assert pistol.x == 2 and pistol.y == 2

    # Tank footprint 2x2
    tank = BaseUnit("t1", UnitType.TANK, Team.PLAYER, 0, 0)
    assert bf.place_unit(tank, 4, 4) is True
    assert bf.get_unit_at(4, 4) == tank
    assert bf.get_unit_at(5, 5) == tank

    # Cannot overlap existing unit
    p2 = BaseUnit("p2", UnitType.PISTOL, Team.ENEMY, 0, 0)
    assert bf.place_unit(p2, 4, 4) is False

