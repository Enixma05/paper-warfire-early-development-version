import pytest
from src.core.constants import Visibility, Team
from src.game.config import UnitType
from src.game.base_unit import BaseUnit
from src.game.fog_of_war import FogOfWarManager

def test_fog_of_war_sight_and_updates():
    fow = FogOfWarManager(cols=24, rows=16, team=Team.PLAYER)
    # Initially all unexplored
    assert fow.get_visibility(5, 5) == Visibility.UNEXPLORED

    # Place friendly sniper (sight range 5) at (5, 5)
    sniper = BaseUnit("s1", UnitType.SNIPER, Team.PLAYER, 5, 5)
    newly_seen = fow.update_visibility([sniper])
    assert newly_seen > 0

    # (5, 5) should be VISIBLE
    assert fow.is_visible(5, 5) is True
    # (10, 5) is at distance 5 -> VISIBLE
    assert fow.is_visible(10, 5) is True
    # (11, 5) is at distance 6 -> UNEXPLORED
    assert fow.is_visible(11, 5) is False

    # Move sniper away to (15, 15)
    sniper.x = 15
    sniper.y = 15
    fow.update_visibility([sniper])

    # Old position (5, 5) should now be EXPLORED (shrouded), not UNEXPLORED
    assert fow.get_visibility(5, 5) == Visibility.EXPLORED
    assert fow.is_visible(5, 5) is False
    assert fow.is_explored(5, 5) is True

    # New position should be VISIBLE
    assert fow.is_visible(15, 15) is True

def test_impact_reveal():
    fow = FogOfWarManager(cols=24, rows=16, team=Team.PLAYER)
    fow.reveal_area(10, 10, radius=1)
    # Center and 8 surrounding should be visible
    assert fow.is_visible(10, 10) is True
    assert fow.is_visible(9, 9) is True
    assert fow.is_visible(11, 11) is True
    assert fow.is_visible(12, 12) is False

