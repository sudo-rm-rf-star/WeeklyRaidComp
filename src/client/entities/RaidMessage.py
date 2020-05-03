import discord
import asyncio

from src.logic.Roster import Roster
from src.client.entities.DiscordMessage import DiscordMessage
from src.client.GuildClient import GuildClient
from src.common.Constants import DATETIMESEC_FORMAT
from src.common.EmojiNames import CALENDAR_EMOJI, CLOCK_EMOJI, TEAM_EMOJI, MISSING_EMOJI, SIGNUPS_EMOJI, ROLE_CLASS_EMOJI, ROLE_EMOJI, SIGNUP_STATUS_EMOJI
from src.logic.RaidEvent import RaidEvent
from src.logic.enums.Role import Role
from src.logic.enums.SignupStatus import SignupStatus
from src.logic.enums.RosterStatus import RosterStatus
from src.logic.Players import Players
from discord import Embed
from typing import List, Optional, Dict, Union

EMPTY_FIELD = '\u200e'


class RaidMessage(DiscordMessage):
    def __init__(self, client: GuildClient, raid_event: RaidEvent):
        self.client = client
        self.raid_event = raid_event
        self.embed = self._raid_to_embed()
        super().__init__(embed=self.embed)

    async def send_to(self, recipient: Union[discord.User, discord.TextChannel]) -> discord.Message:
        message = await super(RaidMessage, self).send_to(recipient)
        for emoji in [emoji_name for status, emoji_name in SIGNUP_STATUS_EMOJI.items() if status != SignupStatus.UNDECIDED]:
            asyncio.create_task(message.add_reaction(emoji=self._get_emoji(emoji)))
        return message

    async def sync(self):
        """Updates the existing RaidMessages if the raid_event has been updated"""
        if self.raid_event.rosters.was_updated():
            messages = await self.get_existing_discord_messages(self.raid_event)
            for message in messages:
                await message.edit(embed=self.embed)

    async def remove(self):
        messages = await self.get_existing_discord_messages(self.raid_event)
        for message in messages:
            await message.delete()

    async def get_existing_discord_messages(self, raid_event: RaidEvent) -> List[discord.Message]:
        """ Find all existing instances which we want to sync """
        return [(await self.client.get_message(msg_id, channel_id)) for (msg_id, channel_id, message_type) in raid_event.message_id_pairs if
                message_type == type(self)]

    def _raid_to_embed(self) -> Embed:
        embed = {'title': self._get_title(),
                 'description': self._get_description(),
                 'fields': self._get_fields(),
                 'footer': self.get_footer(),
                 'color': 2171428,
                 'type': 'rich'}
        return Embed.from_dict(embed)

    def _get_title(self) -> str:
        return f'{self.raid_event.get_name()} op {self.raid_event.get_weekday()}'

    def _get_description(self) -> str:
        return f'{self._get_emoji(CALENDAR_EMOJI)} {self.raid_event.get_date()}\n' \
               f'{self._get_emoji(CLOCK_EMOJI)} {self.raid_event.get_time()}\n' \
               f'{self._get_emoji(SIGNUPS_EMOJI)} {self.raid_event.get_signee_count()}'

    def get_footer(self) -> Optional[Dict[str, str]]:
        return {'text': f'Created at: {self.raid_event.created_at.strftime(DATETIMESEC_FORMAT)}. ' +
                        f'Last updated at: {self.raid_event.updated_at.strftime(DATETIMESEC_FORMAT)}'}

    def _get_fields(self) -> List[Dict[str, str]]:
        fields = []
        for roster_index, roster in enumerate(self.raid_event.rosters):
            team_description = f'{self._get_emoji(TEAM_EMOJI)} **__Team {roster_index + 1}__** ({roster.accepted_count()})\n'
            players_per_role = roster.get_players_per_role()
            fields.extend([
                _field(team_description, inline=False),
                self._get_field_for_role(players_per_role, Role.TANK),
                self._get_field_for_role(players_per_role, Role.HEALER),
                _empty_field(),

                self._get_field_for_role(players_per_role, Role.MELEE),
                self._get_field_for_role(players_per_role, Role.RANGED),
                _empty_field(),

                self._get_missing_field(roster)
            ])
        return fields

    def _get_field_for_role(self, players_per_role: Dict[Role, str], role: Role) -> Dict[str, str]:
        players_for_role = [player_name for player_name in players_per_role[role]
                            if self.raid_event.rosters.get_roster_choice(player_name) != RosterStatus.DECLINE]
        player_lines = '\n'.join(sorted([self._get_player_line(player_name) for player_name in players_for_role]))
        value = f'{self._role_emoji(role)} **__{role.name.capitalize()}__** ({len(players_for_role)}):\n{player_lines}'
        return _field(value)

    def _get_player_line(self, player_name: str) -> str:
        signup_choice = self.raid_event.rosters.signee_choices[player_name]
        roster_choice = self.raid_event.rosters.get_roster_choice(player_name)
        signup_choice_indicator = '' if signup_choice == SignupStatus.ACCEPT else self._signup_choice_emoji(signup_choice)
        if roster_choice == RosterStatus.ACCEPT:
            roster_choice_indicator = ('__', '__')
        elif roster_choice == RosterStatus.EXTRA:
            roster_choice_indicator = ('~~', '~~')
        else:
            roster_choice_indicator = ('', '')
        return f'{self._role_class_emoji(player_name)} {roster_choice_indicator[0]}{player_name}{roster_choice_indicator[1]} {signup_choice_indicator}'

    def _get_missing_field(self, roster: Roster) -> Dict[str, str]:
        missing_roles = roster.missing(self.raid_event.name)
        if len(missing_roles.keys()) == 0:
            return _empty_field(inline=True)
        else:
            value = f'{self._get_emoji(MISSING_EMOJI)} **__{MISSING_EMOJI}__**: {", ".join([f"**{role.capitalize()}** ({count})" for role, count in missing_roles.items()])} '
            return _field(value, inline=True)

    def _role_emoji(self, role: Role) -> discord.Emoji:
        return self._get_emoji(ROLE_EMOJI[role])

    def _role_class_emoji(self, player_name: str) -> discord.Emoji:
        player = Players().get(player_name)
        return self._get_emoji(ROLE_CLASS_EMOJI[player.role][player.klass])

    def _signup_choice_emoji(self, signup_choice: SignupStatus) -> discord.Emoji:
        return self._get_emoji(SIGNUP_STATUS_EMOJI[signup_choice])

    def _get_emoji(self, name: str) -> discord.Emoji:
        return self.client.get_emoji(name)


def _field(content: str, inline: bool = True):
    return {'name': EMPTY_FIELD, 'value': content, 'inline': inline}


def _empty_field(inline: bool = True):
    return _field(EMPTY_FIELD, inline)
