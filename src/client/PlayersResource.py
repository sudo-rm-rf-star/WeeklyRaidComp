from client.DiscordClient import DiscordClient
from persistence.TableFactory import TableFactory
from persistence.PlayersTable import PlayersTable
from logic.Player import Player
from typing import List, Optional


class PlayersResource:
    def __init__(self, client: DiscordClient):
        self.client: DiscordClient = client
        self.players_table: PlayersTable = TableFactory().get_players_table()

    def list_players(self) -> List[Player]:
        return self.players_table.scan()

    def get_player(self, name: str) -> Optional[Player]:
        return self.players_table.get_player(name)

    def get_player_by_id(self, discord_id: int) -> Optional[Player]:
        return self.players_table.get_player_by_id(discord_id)

    def update_player(self, player: Player):
        return self.players_table.put_player(player)

    def remove_player(self, player_name: str) -> bool:
        return self.players_table.remove_player(player_name)
