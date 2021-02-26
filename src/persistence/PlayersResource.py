from persistence.tables.TableFactory import TableFactory
from persistence.tables.PlayersTable import PlayersTable
from logic.Player import Player
from typing import Optional
from exceptions.InvalidInputException import InvalidInputException
from logic.Character import Character
from logic.RaidTeam import RaidTeam
from utils.Singleton import Singleton
import discord


class PlayersResource(metaclass=Singleton):
    def __init__(self):
        self.players_table: PlayersTable = TableFactory().get_players_table()

    def get_player_by_name(self, name: str, raid_team: RaidTeam) -> Optional[Player]:
        return self.players_table.get_player_by_name(name, raid_team)

    def get_player_by_id(self, discord_id: int) -> Optional[Player]:
        return self.players_table.get_player_by_id(discord_id)

    def update_player(self, player: Player):
        return self.players_table.put_player(player)

    def remove_character(self, character: Character):
        self.players_table.remove_character(character)

    def select_character(self, player: Player, char_name: str):
        char_names = [char.name for char in player.characters]
        if not any(x == char_name for x in char_names):
            raise InvalidInputException(
                f"You don't have a character named {char_name}. Your characters are: " + ", ".join(char_names))
        player.selected_char = char_name
        self.update_player(player)

    def select_raidteam(self, guild_member: discord.Member, raidgroup: RaidTeam):
        player = self.get_player_by_id(guild_member.id)
        player.selected_team_name = raidgroup.name
        self.update_player(player)
