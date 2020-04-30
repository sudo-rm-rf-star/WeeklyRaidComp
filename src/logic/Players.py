from src.filehandlers.PlayerFileHandler import load_players, save_players
from src.logic.Player import Player
from typing import Any


class Players:
    class __Players:
        def __init__(self):
            self.players_by_id = {player.discord_id: player for player in load_players()}
            self.players_by_name = {player.name: player for player in self.players_by_id.values()}

        def add(self, player: Player) -> None:
            self.players_by_id[player.discord_id] = player
            self.players_by_name[player.name] = player

        def store(self) -> None:
            save_players(list(self.players_by_id.values()))

        def get(self, player_name) -> Player:
            return self.players_by_name.get(player_name, None)

        def get_by_id(self, player_id) -> Player:
            return self.players_by_id.get(player_id, None)

    instance = None

    def __new__(cls):
        if not Players.instance:
            Players.instance = Players.__Players()
        return Players.instance

    def __getattr__(self, name: str) -> Any:
        return getattr(self.instance, name)

    def __setattr__(self, name: str, **kwargs) -> None:
        return setattr(self.instance, name, **kwargs)
