import json

from gmat_inputs import get_gmat_inputs


SAVE_FILE = "savegame.json"


def save_game(game_state, current_screen="mission_control", filename=SAVE_FILE):
    data = {
        "version": 1,
        "current_screen": current_screen,
        "difficulty": game_state.difficulty,
        "player_count": game_state.player_count,
        "players": [
            {
                "number": player.number,
                "role": player.role,
                "customizations": player.customizations,
            }
            for player in game_state.players
        ],
        "roster": game_state.roster,
        "rocket_tier": game_state.rocket.price_tier if game_state.rocket else None,
        "mission_customizations": game_state.mission_customizations,
    }

    saved_text = json.dumps(data, indent=2)
    with open(filename, "w", encoding="utf-8") as save_file:
        save_file.write(saved_text)


def save_before_simulation(game_state, current_screen="mission_control", filename=SAVE_FILE):
    if game_state.rocket is None:
        raise ValueError("Choose a rocket before starting the simulation")
    gmat_inputs = get_gmat_inputs(game_state)
    save_game(game_state, current_screen, filename)
    return gmat_inputs
