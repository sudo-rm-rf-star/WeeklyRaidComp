import discord
from client.entities.DiscordMessage import DiscordMessage
from typing import List, Dict
from logic.Report import Report
from logic.RaidEvent import RaidEvent
from utils.EmojiNames import CALENDAR_EMOJI, CLOCK_EMOJI
from collections import defaultdict
from logic.enums.RosterStatus import RosterStatus
from logic.enums.SignupStatus import SignupStatus


class RaidConsumablesEvaluationMessage(DiscordMessage):
    def __init__(self, client: discord.Client, guild: discord.Guild, report: Report, raid_event: RaidEvent, consumable_name: str):
        self.report = report
        self.raid_event = raid_event
        self.discord_client = client
        self.discord_guild = guild
        self.consumable_name = consumable_name
        super().__init__(client, guild, embed=self._report_to_embed())

    def _get_title(self) -> str:
        return f'{self.raid_event.get_name()} - {self.consumable_name} Review'

    def _get_description(self) -> str:
        return f'{self._get_emoji(CALENDAR_EMOJI)} {self.raid_event.get_date()} ({self.raid_event.get_weekday().capitalize()})\n' \
               f'{self._get_emoji(CLOCK_EMOJI)} {self.raid_event.get_time()}\n' \
               f'{self.report.buff_url}'

    def _report_to_embed(self) -> discord.Embed:
        embed = {
            'title': self._get_title(),
            'description': self._get_description(),
            'fields': self._get_fields(),
            'color': 2171428,
            'type': 'rich'}
        return discord.Embed.from_dict(embed)

    def _get_fields(self) -> List[Dict[str, str]]:
        all_players_in_raid = set.union(*[fight.present_players for fight in self.report.fights])
        fields = []

        values = []
        buff_count = list(sorted({player: self.report.buff_counts.get(player, 0) for player in all_players_in_raid}.items(), key=lambda x: x[1]))
        for player, count in buff_count:
            values.append(f'{player}: {count}')
        fields.append(self._field('\n'.join(values), inline=False))

        return fields
