from dataclasses import dataclass


@dataclass(frozen=True)
class Role:
    name: str
    description: str


def load_roles():
    try:
        source = open("../MissionControlRoles", encoding="utf-8")
    except FileNotFoundError:
        source = open("MissionControlRoles", encoding="utf-8")

    roles = []
    name = None
    with source:
        for raw_line in source:
            line = raw_line.strip()
            if line.startswith("Name: "):
                name = line.removeprefix("Name: ")
            elif line.startswith("Description: ") and name is not None:
                roles.append(Role(name, line.removeprefix("Description: ")))
                name = None
    return roles
