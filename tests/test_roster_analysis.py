import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from unittest.mock import patch

from roster_analysis import MAX_ANALYSIS_POINTS, analysis_result, roll_analysis, success_chance


class RosterAnalysisTests(unittest.TestCase):
    def test_best_four_define_the_maximum(self):
        self.assertEqual(MAX_ANALYSIS_POINTS, 60)
        roster = ["Geologist", "Physicists", "Astrobiologist", "Geneticist"]
        self.assertEqual(success_chance(roster), 80)
        self.assertEqual(analysis_result(roster, 20), (60, 80, True))

    def test_zero_bonus_can_succeed_or_fail(self):
        roster = ["Signal Engineer", "Psychologist", "Linguist", "Flight Director"]
        self.assertEqual(success_chance(roster), 20)
        self.assertEqual(analysis_result(roster, 79), (0, 79, False))
        self.assertEqual(analysis_result(roster, 80), (0, 80, True))

    def test_crew_bonus_improves_same_roll(self):
        low = ["Signal Engineer", "Psychologist", "Linguist", "Flight Director"]
        high = ["Geologist", "Physicists", "Geneticist", "Astronaut"]
        self.assertFalse(analysis_result(low, 40)[2])
        self.assertTrue(analysis_result(high, 40)[2])

    def test_new_analysis_draws_random_roll(self):
        roster = ["Signal Engineer", "Psychologist", "Linguist", "Flight Director"]
        with patch("roster_analysis.random.randrange", return_value=92) as draw:
            self.assertEqual(roll_analysis(roster), (92, 0, 92, True))
            draw.assert_called_once_with(100)

    def test_roster_requires_four_distinct_known_crew(self):
        for roster in (["Geologist"] * 4, ["Geologist", "Physicists"],
                       ["Geologist", "Physicists", "Geneticist", "Unknown"]):
            with self.subTest(roster=roster), self.assertRaises(ValueError):
                analysis_result(roster, 50)


if __name__ == "__main__":
    unittest.main()
