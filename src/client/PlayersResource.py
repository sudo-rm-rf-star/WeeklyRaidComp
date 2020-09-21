from persistence.TableFactory import TableFactory
from persistence.PlayersTable import PlayersTable
from logic.Player import Player
from logic.RaidGroup import RaidGroup
from typing import List, Optional
from client.entities.GuildMember import GuildMember
from exceptions.InvalidArgumentException import InvalidArgumentException
from logic.Character import Character
from logic.Guild import Guild


class PlayersResource:
    def __init__(self):
        self.players_table: PlayersTable = TableFactory().get_players_table()

    def list_players(self, guild: Guild) -> List[Player]:
        return self.players_table.list_players(guild)

    def get_player_by_name(self, name: str, guild: Guild) -> Optional[Player]:
        return self.players_table.get_player_by_name(name, guild)

    def get_player_by_id(self, discord_id: int) -> Optional[Player]:
        return self.players_table.get_player_by_id(discord_id)

    def update_player(self, player: Player):
        return self.players_table.put_player(player)

    def remove_character(self, character: Character):
        self.players_table.remove_character(character)

    def select_character(self, player: Player, char_name: str):
        char_names = [char.name for char in player.characters]
        if not any(x == char_name for x in char_names):
            raise InvalidArgumentException(f"You don't have a character named {char_name}. Your characters are: " + ", ".join(char_names))
        player.selected_char = char_name
        self.update_player(player)

    def select_raidgroup(self, guild_member: GuildMember, raidgroup: RaidGroup):
        player = self.get_player_by_id(guild_member.id)
        player.selected_raidgroup_id = raidgroup.group_id
        self.update_player(player)
