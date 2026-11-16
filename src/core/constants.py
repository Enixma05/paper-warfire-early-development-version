"""Global constants for Paper Warfire.
Defines screen dimensions, colors, frame rates, and state enums.
"""

from enum import Enum, auto

# Screen & Display Settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TARGET_FPS = 60
WINDOW_TITLE = "Paper Warfire - Simultaneous Turn-Based Strategy"

# Grid Dimensions
GRID_COLS = 24
GRID_ROWS = 16
TILE_SIZE = 40  # 24 * 40 = 960 px width; 16 * 40 = 640 px height
GRID_OFFSET_X = 20
GRID_OFFSET_Y = 60

# Palette (Geometric Minimalist Theme)
COLOR_BG = (37, 40, 48)            # #252830 Dark Slate Background
COLOR_GRID = (85, 91, 102)          # #555B66 Neutral Slate Grid Lines
COLOR_PLAYER = (74, 144, 226)       # #4A90E2 Blue Tactical
COLOR_ENEMY = (224, 82, 82)         # #E05252 Red Alert
COLOR_ACCENT = (242, 193, 78)       # #F2C14E Gold Selection / Targeting
COLOR_TEXT = (229, 231, 235)        # #E5E7EB Off-White
COLOR_TEXT_DIM = (156, 163, 175)    # #9CA3AF Dim Gray
COLOR_PANEL_BG = (28, 30, 36)       # #1C1E24 Dark Panel Background
COLOR_PANEL_BORDER = (55, 60, 70)   # Border Gray

# Fog of War Colors
COLOR_FOG_UNEXPLORED = (15, 17, 22) # Pitch black / very dark
COLOR_FOG_EXPLORED = (25, 28, 35)   # Shrouded / dimmed terrain

# Terrain Colors (Distinct, high-contrast palette)
COLOR_TERRAIN_PLAINS = (68, 98, 70)      # Natural Grass Plains
COLOR_TERRAIN_FOREST = (30, 72, 40)      # Deep Forest Foliage
COLOR_TERRAIN_MOUNTAIN = (120, 125, 135) # Rocky Mountain (Impassable)
COLOR_TERRAIN_WATER = (42, 95, 145)      # Water Hazard / River

# Global Game States
class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSE = auto()
    VICTORY = auto()
    DEFEAT = auto()


# WEGO Turn Sub-states (within PLAYING state)
class TurnSubState(Enum):
    PLANNING = auto()       # Orders being planned by Player & AI
    WAR_EXECUTION = auto()  # Simultaneous execution (Movement -> Combat -> FoW)
    SUMMARY = auto()        # Turn rewards, upgrade shop, win/lose checks


# Teams
class Team(Enum):
    PLAYER = auto()
    ENEMY = auto()


# Visibility States for Fog of War
class Visibility(Enum):
    UNEXPLORED = 0  # Pitch black, completely unknown
    EXPLORED = 1    # Terrain is known, but units are invisible
    VISIBLE = 2     # Actively visible by friendly unit or impact

