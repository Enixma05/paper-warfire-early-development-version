"""Entry point for Paper Warfire.
Launches the 2D Grid-Based Turn-Based Strategy game engine.
"""

import sys
import os

# Add root directory to python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.core.engine import GameEngine

def main():
    headless = "--headless" in sys.argv
    if headless:
        os.environ["SDL_VIDEODRIVER"] = "dummy"

    engine = GameEngine(headless=headless)
    if headless:
        print("Paper Warfire launched in headless smoke-test mode.")
        # Perform 10-tick smoke test
        engine.start_game()
        for _ in range(10):
            engine._update(0.016)
            engine._render()
        print("Smoke test passed successfully!")
    else:
        engine.run()

if __name__ == "__main__":
    main()

