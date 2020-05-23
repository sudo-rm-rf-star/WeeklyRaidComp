from client.DiscordClient import DiscordClient
from persistence.TableFactory import TableFactory
from persistence.PlayersTable import PlayersTable
from logic.Player import Player
from typing import List, Optional
from datetime import datetime


class PlayersResource:
    def __init__(self, client: DiscordClient):
        self.client: DiscordClient = client
        self.players_table: PlayersTable = TableFactory().get_players_table()

    def list_characters(self) -> List[Player]:
        return self.players_table.scan()

    def get_character(self, name: str) -> Optional[Player]:
        return self.players_table.get_player(name)

    def get_character_by_id(self, discord_id: int) -> Optional[Player]:
        return self.get_selected_character(self.get_characters_by_id(discord_id))

    def get_characters_by_id(self, discord_id: int) -> List[Player]:
        return self.players_table.get_players_by_id(discord_id)

    def update_character(self, player: Player):
        return self.players_table.put_player(player)

    def remove_character(self, player_name: str) -> bool:
        return self.players_table.remove_player(player_name)

    def select_character(self, player_name: str) -> bool:
        player = self.get_character(player_name)
        if not player:
            return False
        player.last_selected_time = datetime.now()
        self.update_character(player)
        return True

    def get_selected_character(self, players: List[Player]) -> Optional[Player]:
        if len(players) == 0:
            return None
        elif all(player.last_selected_time is None for player in players):
            return players[0]
        else:
            return max([player for player in players if player.last_selected_time],
                       key=lambda player: player.last_selected_time)


