import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from game_state import GameState


class GameStateTests(unittest.TestCase):
    def test_roster_locks_after_selection_and_reset_clears_everything(self):
        state = GameState()
        state.difficulty = "First Ascent"
        state.set_player_count(2)
        state.players[0].role = "Geologist"
        state.roster = ["Geologist", "Physicists", "Astrobiologist", "Astronaut"]
        state.roster_locked = True
        state.rocket = object()
        state.mission_customizations["instruments"] = {"Food": 2}

        state.toggle_roster_position("Geologist")
        self.assertEqual(len(state.roster), 4)

        state.reset()
        self.assertIsNone(state.difficulty)
        self.assertIsNone(state.player_count)
        self.assertEqual(state.players, [])
        self.assertEqual(state.roster, [])
        self.assertFalse(state.roster_locked)
        self.assertIsNone(state.rocket)
        self.assertEqual(state.mission_customizations, {})


if __name__ == "__main__":
    unittest.main()
