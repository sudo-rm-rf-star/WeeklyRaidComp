import discord
from client.entities.DiscordMessage import DiscordMessage
from typing import List, Dict
from logic.Report import Report
from logic.RaidEvent import RaidEvent
from utils.EmojiNames import CALENDAR_EMOJI, CLOCK_EMOJI
from utils.Consumables import CONSUMABLE_REQUIREMENTS


class RaidConsumablesEvaluationMessage(DiscordMessage):
    def __init__(self, client: discord.Client, guild: discord.Guild, report: Report, raid_event: RaidEvent):
        self.report = report
        self.raid_event = raid_event
        self.discord_client = client
        self.discord_guild = guild
        super().__init__(client, guild, embed=self._report_to_embed())

    def _get_title(self) -> str:
        return f'{self.raid_event.get_name()} - Consumables Review'

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
        characters_in_raid = set.union(*[fight.present_players for fight in self.report.fights])
        characters_by_name = {char.name: char for char in self.raid_event.get_signed_characters()}
        fields = []

        buff_counts = self.report.buff_counts
        for consumable_requirements in CONSUMABLE_REQUIREMENTS[self.raid_event.name]:
            consumables = consumable_requirements.consumable_names
            player_counts = buff_counts.get(tuple(consumables), {})
            buff_count = list(
                sorted({char_name: player_counts.get(char_name, 0) for char_name in characters_in_raid}.items(),
                       key=lambda x: -x[1]))
            values = [f'**{", ".join(consumables)}**']
            for char_name, count in buff_count:
                character = characters_by_name.get(char_name)
                if character:
                    has_role = character.role in consumable_requirements.roles
                    has_class = character.klass in consumable_requirements.classes
                    has_role_class = (character.role, character.klass) in consumable_requirements.role_classes
                    if has_class or has_role or has_role_class:
                        role_class_emoji = self._role_class_emoji(character) if character is not None else ''
                        values.append(f'{role_class_emoji} {char_name}: {count}')
            fields.extend(self.split_column_evenly(values))
        return fields
