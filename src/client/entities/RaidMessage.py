import discord

from exceptions.InternalBotException import InternalBotException
from client.entities.DiscordMessage import DiscordMessage
from client.DiscordClient import DiscordClient
from utils.Constants import DATETIMESEC_FORMAT
from utils.EmojiNames import CALENDAR_EMOJI, CLOCK_EMOJI, TEAM_EMOJI, MISSING_EMOJI, SIGNUPS_EMOJI, ROLE_CLASS_EMOJI, ROLE_EMOJI, SIGNUP_STATUS_EMOJI
from logic.RaidEvent import RaidEvent
from logic.enums.Role import Role
from logic.enums.SignupStatus import SignupStatus
from logic.enums.RosterStatus import RosterStatus
from logic.RaidComposition import actual_vs_expected_per_role
from discord import Embed
from typing import List, Optional, Dict, Union
from logic.Player import Player
import asyncio

EMPTY_FIELD = '\u200e'


class RaidMessage(DiscordMessage):
    def __init__(self, client: DiscordClient, raid_event: RaidEvent):
        self.client = client
        self.raid_event = raid_event
        self.raid_players = raid_event.roster.players
        self.embed = self._raid_to_embed()
        super().__init__(embed=self.embed)

    async def send_to(self, recipient: Union[discord.User, discord.TextChannel]) -> discord.Message:
        msgs = await super(RaidMessage, self).send_to(recipient)
        if len(msgs) > 1:
            raise InternalBotException("Unhandled case")
        return msgs[0]

    def sync(self):
        """Updates the existing RaidMessages if the raid_event has been updated"""
        if self.raid_event.roster.was_updated():
            for message_id in self.raid_event.message_ids:
                asyncio.create_task(_update_message(self.client, message_id, self.embed))

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
               f'{self._get_emoji(SIGNUPS_EMOJI)} {signed_and_not_declined_count(self.raid_players)}'

    def get_footer(self) -> Optional[Dict[str, str]]:
        return {'text': f'Created at: {self.raid_event.created_at.strftime(DATETIMESEC_FORMAT)}. ' +
                        f'Last updated at: {self.raid_event.updated_at.strftime(DATETIMESEC_FORMAT)}'}

    def _get_fields(self) -> List[Dict[str, str]]:
        fields = []
        for team_index, raid_team in enumerate(self.raid_event.roster.team_iter()):
            team_description = f'{self._get_emoji(TEAM_EMOJI)} **__Team {team_index + 1}__** ({roster_accepted_count(raid_team)})\n'
            fields.extend([
                _field(team_description, inline=False),
                self._get_field_for_role(raid_team, Role.TANK),
                self._get_field_for_role(raid_team, Role.HEALER),
                _empty_field(),

                self._get_field_for_role(raid_team, Role.MELEE),
                self._get_field_for_role(raid_team, Role.RANGED),
                _empty_field(),

                self._get_summary_field(raid_team),
            ])
        fields.extend([
            self._get_declined_field()
        ])
        return fields

    def _get_field_for_role(self, raid_team: List[Player], role: Role) -> Dict[str, str]:
        players = [player for player in raid_team if player.role == role and not player.is_declined()]
        player_lines = '\n'.join(sorted([self._get_player_line(player) for player in players]))
        value = f'{self._role_emoji(role)} **__{role.name.capitalize()}__** ({len(players)}):\n{player_lines}'
        return _field(value)

    def _get_player_line(self, player: Player) -> str:
        signup_choice = player.signup_status
        roster_choice = player.roster_status
        signup_choice_indicator = '' if signup_choice == SignupStatus.ACCEPT else self._signup_choice_emoji(signup_choice)
        if roster_choice == RosterStatus.ACCEPT:
            roster_choice_indicator = ('__', '__')
        elif roster_choice == RosterStatus.EXTRA:
            roster_choice_indicator = ('~~', '~~')
        else:
            roster_choice_indicator = ('', '')
        return f'{self._role_class_emoji(player)} {roster_choice_indicator[0]}{player.name}{roster_choice_indicator[1]} {signup_choice_indicator}'

    def _get_summary_field(self, raid_team) -> Dict[str, str]:
        summary = ", ".join([f"**{role.capitalize()}** ({actual/expected})" for role, (actual, expected) in actual_vs_expected_per_role(self.raid_event.name, raid_team)])
        value = f'{self._get_emoji(MISSING_EMOJI)} **__{MISSING_EMOJI}__**: {summary}'
        return _field(value, inline=False)

    def _get_declined_field(self):
        value = f'**Declined**: {", ".join([player.name for player in self.raid_players if player.is_declined()])}'
        return _field(value, inline=False)

    def _role_emoji(self, role: Role) -> discord.Emoji:
        return self._get_emoji(ROLE_EMOJI[role])

    def _role_class_emoji(self, player: Player) -> discord.Emoji:
        return self._get_emoji(ROLE_CLASS_EMOJI[player.role][player.klass])

    def _signup_choice_emoji(self, signup_choice: SignupStatus) -> discord.Emoji:
        return self._get_emoji(SIGNUP_STATUS_EMOJI[signup_choice])

    def _get_emoji(self, name: str) -> discord.Emoji:
        return self.client.get_emoji(name)


def _field(content: str, inline: bool = True):
    return {'name': EMPTY_FIELD, 'value': content, 'inline': inline}


def _empty_field(inline: bool = True):
    return _field(EMPTY_FIELD, inline)


def signed_and_not_declined_count(players: List[Player]) -> int:
    return sum(1 for player in players if player.signup_status != SignupStatus.DECLINE and player.roster_status != RosterStatus.DECLINE)


def roster_accepted_count(players: List[Player]) -> int:
    return sum(1 for player in players if player.roster_status == RosterStatus.ACCEPT)


async def _update_message(client, message_id, embed):
    message = await client.get_message(message_id)
    await message.edit(embed=embed)
