import json
import math
import os
import re
import subprocess
import sys
import uuid


def _project_config():
    with open("../gmat_config.json", encoding="utf-8") as config_file:
        return json.load(config_file)


def _parse_trajectory(report_file):
    trajectory = []
    with open(report_file, encoding="utf-8") as result_file:
        for line in result_file:
            columns = line.split()
            if len(columns) < 8:
                continue
            try:
                point = tuple(map(float, columns[:8]))
            except ValueError:
                continue
            if all(math.isfinite(value) for value in point):
                trajectory.append(point)
    if len(trajectory) < 2:
        raise RuntimeError("GMAT did not produce enough reference trajectory data")
    return trajectory


def run_gmat_simulation(inputs):
    # Spacecraft inputs remain part of the game/save flow, but the mission is fixed.
    return run_lunar_transfer_demo()


def run_lunar_transfer_demo():
    config = _project_config()
    bin_dir = os.path.abspath(config["bin_dir"])
    output_dir = os.path.abspath(config["output_dir"])
    sample_file = os.path.join(bin_dir, "..", "samples", "NeedOpenFramesInterface", "Ex_OFI_LunarTransfer.script")
    report_file = os.path.join(output_dir, "lunar_transfer_reference_trajectory.txt")
    script_file = os.path.join(output_dir, "lunar_transfer_reference_" + uuid.uuid4().hex[:12] + ".script")

    with open(sample_file, encoding="utf-8") as source:
        script = source.read()
    # Keep the sample mission intact while letting gmatpy run without its GUI subscribers.
    script = re.sub(
        r"(?ms)^Create (?:OpenFramesInterface|OpenFramesView|XYPlot)\b.*?(?=^Create |^%--- Mission Sequence|^BeginMissionSequence)",
        "",
        script,
    )
    script = "\n".join(line for line in script.splitlines() if "Toggle OFI_" not in line)
    script = script.replace("ShowProgressWindow = true", "ShowProgressWindow = false")
    report_setup = (
        "Create ReportFile MoonbreakersReport;\n"
        f"MoonbreakersReport.Filename = '{report_file.replace(os.sep, '/')}';\n"
        "MoonbreakersReport.Precision = 16;\n"
        "MoonbreakersReport.WriteHeaders = Off;\n"
        "MoonbreakersReport.Add = {Sat.A1ModJulian, Sat.EarthMJ2000Eq.X, Sat.EarthMJ2000Eq.Y, Sat.EarthMJ2000Eq.Z, Sat.MoonMJ2000Eq.X, Sat.MoonMJ2000Eq.Y, Sat.MoonMJ2000Eq.Z, Sat.Luna.RMAG};\n"
    )
    marker = "BeginMissionSequence;"
    if marker not in script:
        raise RuntimeError("Installed Ex_OFI_LunarTransfer script has no mission sequence")
    script = script.replace(marker, report_setup + marker, 1)
    with open(script_file, "w", encoding="utf-8") as destination:
        destination.write(script)

    worker = os.path.join(os.path.dirname(__file__), "gmat_worker.py")
    try:
        completed = subprocess.run(
            [sys.executable, worker, bin_dir, script_file],
            cwd=bin_dir,
            capture_output=True,
            text=True,
            timeout=900,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise RuntimeError("GMAT reference mission exceeded the 15 minute run limit") from error
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "").strip()
        raise RuntimeError("GMAT Python API worker failed" + (f": {detail[-600:]}" if detail else ""))

    return {
        "trajectory": _parse_trajectory(report_file),
        "assessment": None,
        "outcome": "Fixed NASA Ex_OFI_LunarTransfer reference mission",
    }
