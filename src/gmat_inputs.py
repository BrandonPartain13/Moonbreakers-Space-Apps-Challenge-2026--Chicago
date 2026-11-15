import math


REQUIRED_INPUTS = (
    "dry_mass_kg",
    "tank_count",
    "fuel_per_tank_kg",
    "thruster_count",
    "thrust_per_thruster_n",
    "specific_impulse_s",
    "duty_cycle_percent",
    "burn_duration_s",
    "orbit_altitude_km",
    "burn_angle_deg",
)

PARKING_ORBIT_ALTITUDE_KM = 200


def get_gmat_inputs(game_state):
    values = game_state.mission_customizations.get("spacecraft", {})
    if not isinstance(values, dict):
        raise ValueError("Spacecraft inputs are missing")

    inputs = {}
    for key in REQUIRED_INPUTS:
        value = values.get(key)
        if not isinstance(value, str) or not value:
            raise ValueError(f"Missing spacecraft input: {key}")
        try:
            number = float(value)
        except ValueError as error:
            raise ValueError(f"Invalid spacecraft input: {key}") from error
        if not math.isfinite(number):
            raise ValueError(f"Invalid spacecraft input: {key}")
        if key in ("tank_count", "thruster_count"):
            if not value.isdigit() or not 1 <= int(value) <= 4:
                raise ValueError(f"Invalid spacecraft input: {key}")
            inputs[key] = int(value)
        elif key == "burn_angle_deg":
            if not 0 <= number < 360:
                raise ValueError(f"Invalid spacecraft input: {key}")
            inputs[key] = number
        elif key == "orbit_altitude_km":
            if not 180 <= number <= 500:
                raise ValueError("Parking orbit altitude must be between 180 and 500 km")
            inputs[key] = number
        else:
            if number <= 0:
                raise ValueError(f"Invalid spacecraft input: {key}")
            if key == "duty_cycle_percent" and number > 100:
                raise ValueError(f"Invalid spacecraft input: {key}")
            inputs[key] = number
    return inputs
