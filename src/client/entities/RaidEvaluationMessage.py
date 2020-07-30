import discord
from client.entities.DiscordMessage import DiscordMessage
from typing import List, Dict
from logic.Report import Report
from logic.RaidEvent import RaidEvent
from utils.EmojiNames import CALENDAR_EMOJI, CLOCK_EMOJI
from collections import defaultdict
from logic.enums.RosterStatus import RosterStatus
from logic.enums.SignupStatus import SignupStatus


class RaidEvaluationMessage(DiscordMessage):
    def __init__(self, client: discord.Client, guild: discord.Guild, report: Report, raid_event: RaidEvent):
        self.report = report
        self.raid_event = raid_event
        self.discord_client = client
        self.discord_guild = guild
        super().__init__(client, guild, embed=self._report_to_embed())

    def _get_title(self) -> str:
        return f'{self.raid_event.get_name()} - Review'

    def _get_description(self) -> str:
        return f'{self._get_emoji(CALENDAR_EMOJI)} {self.raid_event.get_date()} ({self.raid_event.get_weekday().capitalize()})\n' \
               f'{self._get_emoji(CLOCK_EMOJI)} {self.raid_event.get_time()}\n' \
               f'{self.report.get_url()}'

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
        inactive_fights_per_player = defaultdict(list)
        fields = []

        for fight in self.report.fights:
            inactive_players = all_players_in_raid.difference(fight.present_players)
            for player in inactive_players:
                inactive_fights_per_player[player].append(fight.name)

        player_signup_status = {char.name: char.signup_status for char in self.raid_event.get_signed_characters()}
        accepted_characters = {char.name for char in self.raid_event.get_signed_characters() if char.roster_status == RosterStatus.ACCEPT}
        accepted_but_not_present_players = accepted_characters.difference(all_players_in_raid)

        if len(accepted_but_not_present_players) > 0:
            player_lines = "\n".join([f'{self._signup_choice_emoji(player_signup_status.get(player, SignupStatus.UNDECIDED))} {player}' for player in accepted_but_not_present_players])
            fields.append(self._field(f"**These players were accepted but did not participate**:\n{player_lines}"))

        if len(inactive_fights_per_player) > 0:
            values = ['**These players were inactive during one or more boss fights**:']
            for player, fight_names in sorted(inactive_fights_per_player.items(), key=lambda x: -len(x[1])):
                values.append(f'{self._signup_choice_emoji(player_signup_status.get(player, SignupStatus.UNDECIDED))} {player} ({len(fight_names)}): {", ".join(fight_names)}')
            fields.append(self._field("\n".join(values), inline=False))

        values = ["**Killing time**:"]
        for fight in self.report.fights:
            values.append(f'{fight.name}: {fight.end_time - fight.start_time} seconds')
        fields.append(self._field('\n'.join(values), inline=False))

        values = ["**Time passed after each kill**:"]
        for fight in self.report.fights:
            values.append(f'{fight.name}: {fight.end_time // 60} mins')
        fields.append(self._field('\n'.join(values), inline=False))

        return fields
