import json

from rocket import CheapRocket, MediumRocket, ExpensiveRocket
from roles import load_roles
from save import SAVE_FILE


ROCKET_TYPES = {
    "cheap": CheapRocket,
    "medium": MediumRocket,
    "expensive": ExpensiveRocket,
}
SAVE_SCREENS = (
    "rocket_builder",
    "rocket_configuration",
    "spacecraft_setup",
    "instrumentation",
    "launch",
)


def load_game(game_state, filename=SAVE_FILE):
    with open(filename, encoding="utf-8") as save_file:
        data = json.load(save_file)

    if not isinstance(data, dict):
        raise ValueError("Invalid save file")
    if data.get("version") != 1:
        raise ValueError("Unsupported save file version")

    difficulty = data.get("difficulty")
    player_count = data.get("player_count")
    players = data.get("players")
    roster = data.get("roster")
    rocket_tier = data.get("rocket_tier")
    current_screen = data.get("current_screen", "mission_control")
    if current_screen == "food_needs":
        current_screen = "instrumentation"
    elif current_screen == "mission_control":
        current_screen = "launch"
    if difficulty not in ("Clear skies", "First Ascent", "No mercy"):
        raise ValueError("Invalid difficulty in save file")
    if type(player_count) is not int or not 1 <= player_count <= 4:
        raise ValueError("Invalid player count in save file")
    if not isinstance(players, list) or len(players) != player_count:
        raise ValueError("Invalid players in save file")
    if (not isinstance(roster, list) or len(roster) != 4
            or any(not isinstance(position, str) for position in roster)
            or len(set(roster)) != len(roster)):
        raise ValueError("Invalid roster in save file")
    if not isinstance(rocket_tier, str) or rocket_tier not in ROCKET_TYPES:
        raise ValueError("Invalid rocket in save file")
    if current_screen not in SAVE_SCREENS:
        raise ValueError("Invalid screen in save file")

    loaded_players = []
    assigned_roles = set()
    known_roles = {role.name for role in load_roles()}
    for index, player_data in enumerate(players):
        if not isinstance(player_data, dict) or player_data.get("number") != index + 1:
            raise ValueError("Invalid player in save file")
        role = player_data.get("role")
        customizations = player_data.get("customizations", {})
        if not isinstance(role, str) or role not in known_roles or role in assigned_roles:
            raise ValueError("Invalid player role in save file")
        if not isinstance(customizations, dict):
            raise ValueError("Invalid player customization in save file")
        assigned_roles.add(role)
        loaded_players.append((role, customizations))

    mission_customizations = data.get("mission_customizations", {})
    if not isinstance(mission_customizations, dict):
        raise ValueError("Invalid mission customization in save file")
    spacecraft_values = mission_customizations.get("spacecraft", {})
    if not isinstance(spacecraft_values, dict) or any(
            not isinstance(key, str) or not isinstance(value, str)
            for key, value in spacecraft_values.items()
    ):
        raise ValueError("Invalid spacecraft input in save file")
    instruments = mission_customizations.get("instruments", {})
    known_instruments = {
        "Hyperspectral Imager", "X-Ray Spectrometer", "Infrared (Thermal) Camera",
        "Lunar Magnetometer", "Food", "Star Trackers", "Flash LIDAR System",
        "Ka-Band Radar Altimeter", "Deep-Space Transponder", "Radiation Dosimeter",
        "Cabin Atmosphere Monitor",
        "Infrared Camera", "Star Tracker", "Radiation-Hardened IMU", "Ka-Band Radar",
        "Radiation Dosimeters", "Biometric Health Monitors",
        "X-ray spectrometer", "Infrared camera", "Lunar magnetometer", "Camera"
    }
    if isinstance(instruments, list):
        if any(not isinstance(name, str) or name not in known_instruments for name in instruments) or len(instruments) != len(set(instruments)):
            raise ValueError("Invalid instruments in save file")
    elif isinstance(instruments, dict):
        if any(not isinstance(name, str) or name not in known_instruments
               or type(quantity) is not int or quantity < 0
               for name, quantity in instruments.items()):
            raise ValueError("Invalid instruments in save file")
    else:
        raise ValueError("Invalid instruments in save file")
    # Keep old saves loadable, but drop this option now that it is retired.
    if isinstance(instruments, dict):
        instruments.pop("Cabin Atmosphere Monitor", None)
    else:
        mission_customizations["instruments"] = [
            name for name in instruments if name != "Cabin Atmosphere Monitor"
        ]
    rocket_parts = mission_customizations.get("rocket_parts", {})
    known_parts = {"Main Cryogenic Engines", "Lunar Lander Descent Engine", "RCS Thruster Pod",
                   "Cryogenic Propellant Tanks", "Thermal Protection Heat Shield",
                   "Multi-Layer Insulation (MLI)", "Landing Legs",
                   "Lunar Lander Descent", "Thruster Pods"}
    if (not isinstance(rocket_parts, dict)
            or any(not isinstance(name, str) or name not in known_parts
                   or type(quantity) is not int or quantity < 0
                   for name, quantity in rocket_parts.items())):
        raise ValueError("Invalid rocket parts in save file")
    resources = mission_customizations.get("resources", {})
    if (not isinstance(resources, dict)
            or any(not isinstance(key, str) or not isinstance(value, str)
                   for key, value in resources.items())):
        raise ValueError("Invalid resources in save file")

    game_state.set_player_count(player_count)
    game_state.difficulty = difficulty
    for player, (role, customizations) in zip(game_state.players, loaded_players):
        player.role = role
        player.customizations = customizations
    game_state.roster = roster
    game_state.rocket = ROCKET_TYPES[rocket_tier]()
    game_state.mission_customizations = mission_customizations
    return current_screen
