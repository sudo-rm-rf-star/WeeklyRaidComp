import discord
from client.entities.DiscordMessage import DiscordMessage
from client.entities.GuildMember import GuildMember
from utils.EmojiNames import SIGNUPS_EMOJI
from logic.enums.Role import Role
from logic.Player import Player
from logic.Character import Character
from typing import List, Dict
from datetime import datetime

EMPTY_FIELD = '\u200e'

MAX_CHARACTERS_PER_FIELD = 10  # Any field has a max amount of 1024 characters


class ShowPlayerActivityMessage(DiscordMessage):
    def __init__(self, discord_client: discord.Client, discord_guild: discord.Guild, players: List[Player], raiders: List[GuildMember]):
        self.discord_guild = discord_guild
        self.discord_client = discord_client
        self.raiders = raiders
        self.raider_ids = [raider.id for raider in raiders]
        self.players = [player for player in players if player.discord_id in self.raider_ids]
        self.days_since_last_raid = self._get_days_since_last_raid_per_character()
        self.characters = sorted([char for player in self.players for char in player.characters],
                                 key=lambda char: -self.days_since_last_raid[char])
        self.embed = self._players_to_embed()
        super().__init__(discord_client, discord_guild, embed=self.embed)

    def _players_to_embed(self) -> discord.Embed:
        embed = {'title': self._get_title(),
                 'fields': self._get_fields(),
                 'color': 2171428,
                 'type': 'rich'}
        return discord.Embed.from_dict(embed)

    def _get_title(self) -> str:
        return f'Days since last active:'

    def _get_fields(self) -> List[Dict[str, str]]:
        i = 0
        fields = []
        while i < len(self.characters):
            chars = self.characters[i:i + MAX_CHARACTERS_PER_FIELD]
            player_lines = '\n'.join([self._get_char_line(char) for char in chars])
            fields.append(self._field(player_lines, inline=True))
            i += MAX_CHARACTERS_PER_FIELD
        while len(fields) % 3 != 0:
            fields.append(self._empty_field(inline=True))
        return fields

    def _get_char_line(self, character: Character) -> str:
        return f'{self.days_since_last_raid[character]} - {character.name} {self._role_class_emoji(character)}'

    def _get_days_since_last_raid_per_character(self):
        days_since_last_raid_per_character = {}
        for player in self.players:
            present_dates = {datetime.fromtimestamp(date) for dates in player.present_dates.values() for date in dates}
            days_since_last_raid = (datetime.now() - max(present_dates)).days if present_dates else float("inf")
            for character in player.characters:
                days_since_last_raid_per_character[character] = days_since_last_raid
        return days_since_last_raid_per_character
