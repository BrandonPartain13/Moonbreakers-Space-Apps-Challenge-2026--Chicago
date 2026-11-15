"""How the four selected crew members affect mission data analysis."""

import random

ANALYSIS_POINTS = {
    "Geologist": 20,
    "Physicists": 15,
    "Astrobiologist": 15,
    "Signal Engineer": 0,
    "Astronaut": 5,
    "Doctor": 5,
    "Psychologist": 0,
    "Geneticist": 10,
    "Epidemiologist": 0,
    "Computer Scientist/Engineer": 5,
    "Linguist": 0,
    "Flight Director": 0,
    "Propulsion Engineer": 0,
}

CREW_SIZE = 4
MAX_ANALYSIS_POINTS = sum(sorted(ANALYSIS_POINTS.values(), reverse=True)[:CREW_SIZE])
SUCCESS_TARGET = 80


def roster_points(roster):
    """Return the contribution from selected crew members."""
    if any(member not in ANALYSIS_POINTS for member in roster):
        raise ValueError("Unknown crew member in analysis roster")
    return sum(ANALYSIS_POINTS[member] for member in roster)


def success_chance(roster):
    """A 0-99 roll plus the roster points must reach 80."""
    return max(0, min(100, 100 - max(0, SUCCESS_TARGET - roster_points(roster))))


def analysis_result(roster, roll):
    """Return roster points, combined score, and success for one roll."""
    if len(roster) != CREW_SIZE or len(set(roster)) != CREW_SIZE:
        raise ValueError("Select four different crew members for analysis")
    if type(roll) is not int or not 0 <= roll < 100:
        raise ValueError("Analysis roll must be between 0 and 99")
    points = roster_points(roster)
    total = roll + points
    return points, total, total >= SUCCESS_TARGET


def roll_analysis(roster):
    """Make one fresh random draw for a new mission analysis."""
    roll = random.randrange(100)
    points, total, successful = analysis_result(roster, roll)
    return roll, points, total, successful
