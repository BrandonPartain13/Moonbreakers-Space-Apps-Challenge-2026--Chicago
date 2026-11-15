from dataclasses import dataclass, field

from player import Player
from rocket import Rocket


@dataclass
class GameState:
    difficulty: str | None = None
    player_count: int | None = None
    players: list[Player] = field(default_factory=list)
    roster: list[str] = field(default_factory=list)
    rocket: Rocket | None = None
    mission_customizations: dict = field(default_factory=dict)

    def set_player_count(self, count: int):
        if not 1 <= count <= 4:
            raise ValueError("Player count must be between 1 and 4")
        self.players = [
            self.players[index] if index < len(self.players) else Player(index + 1)
            for index in range(count)
        ]
        self.player_count = count

    def assign_role(self, player_number: int, role: str):
        if any(player.role == role and player.number != player_number for player in self.players):
            raise ValueError(f"{role} is already assigned")
        self.players[player_number - 1].role = role

    def toggle_roster_position(self, position: str):
        if position in self.roster:
            self.roster.remove(position)
        elif len(self.roster) < 4:
            self.roster.append(position)
