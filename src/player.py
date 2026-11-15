from dataclasses import dataclass, field


@dataclass
class Player:
    number: int
    role: str | None = None
    customizations: dict = field(default_factory=dict)
