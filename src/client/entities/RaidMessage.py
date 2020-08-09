from exceptions.InternalBotException import InternalBotException
from client.entities.DiscordMessage import DiscordMessage
from utils.Constants import DATETIMESEC_FORMAT
from utils.EmojiNames import CALENDAR_EMOJI, CLOCK_EMOJI, TEAM_EMOJI, SIGNUPS_EMOJI
from logic.RaidEvent import RaidEvent
from logic.enums.Role import Role
from logic.enums.SignupStatus import SignupStatus
from logic.enums.RosterStatus import RosterStatus
from discord import Embed
from typing import List, Optional, Dict, Union
import asyncio
import discord
from logic.Character import Character


class RaidMessage(DiscordMessage):
    def __init__(self, discord_client: discord.Client, discord_guild: discord.Guild, raid_event: RaidEvent):
        self.discord_client = discord_client
        self.raid_event = raid_event
        self.raid_players = raid_event.roster.characters
        self.discord_guild = discord_guild
        self.embed = self._raid_to_embed()
        super().__init__(discord_client, discord_guild, embed=self.embed)

    async def send_to(self, recipient: Union[discord.User, discord.TextChannel]) -> discord.Message:
        msgs = await super(RaidMessage, self).send_to(recipient)
        if len(msgs) > 1:
            raise InternalBotException("Unhandled case")
        return msgs[0]

    def sync(self):
        """Updates the existing RaidMessages"""
        for message_ref in self.raid_event.message_refs:
            asyncio.create_task(self._update_message(message_ref))

    def _raid_to_embed(self) -> Embed:
        embed = {'title': self._get_title(),
                 'description': self._get_description(),
                 'fields': self._get_fields(),
                 'footer': self.get_footer(),
                 'color': 2171428,
                 'type': 'rich'}
        return Embed.from_dict(embed)

    def _get_title(self) -> str:
        return f'{self.raid_event.get_name()}'

    def _get_description(self) -> str:
        return f'{self._get_emoji(CALENDAR_EMOJI)} {self.raid_event.get_date()} ({self.raid_event.get_weekday().capitalize()})\n' \
               f'{self._get_emoji(CLOCK_EMOJI)} {self.raid_event.get_time()}\n'

    def get_footer(self) -> Optional[Dict[str, str]]:
        return {'text': f'Created at: {self.raid_event.created_at.strftime(DATETIMESEC_FORMAT)}. ' +
                        f'Last updated at: {self.raid_event.updated_at.strftime(DATETIMESEC_FORMAT)}'}

    def _get_fields(self) -> List[Dict[str, str]]:
        raid_team = self.raid_event.roster.get_team()
        characters_by_status = {roster_status: [] for roster_status in RosterStatus}
        for character in raid_team:
            characters_by_status[character.roster_status].append(character)

        fields = []
        for roster_status in [RosterStatus.ACCEPT, RosterStatus.UNDECIDED, RosterStatus.EXTRA, RosterStatus.DECLINE]:
            characters = [char for char in characters_by_status[roster_status] if not char.is_declined()]
            if len(characters) > 0:
                fields.append(self._get_title_for_roster_status(characters, roster_status))
                field_count = 0
                for role in [Role.TANK, Role.HEALER, Role.MELEE, Role.RANGED]:
                    field = self._get_field_for_role(characters, role)
                    if field:
                        fields.append(field)
                        field_count += 1
                    if field_count == 2:
                        fields.append(self._empty_field())
                        field_count = 0
                while field_count != 3:
                    fields.append(self._empty_field())
                    field_count += 1

        return fields

    def _get_title_for_roster_status(self, characters: List[Character], roster_status: RosterStatus):
        title = {
            RosterStatus.ACCEPT: "Accepted",
            RosterStatus.EXTRA: "Standby",
            RosterStatus.DECLINE: "Declined",
            RosterStatus.UNDECIDED: "Undecided"
        }
        return self._field(f"**__{title[roster_status]}__** ({len(characters)})", inline=False)

    def _get_field_for_role(self, characters: List[Character], role: Role) -> Optional[Dict[str, str]]:
        characters = [character for character in characters if character.role == role]
        if len(characters) == 0:
            return None
        player_lines = '\n'.join(sorted([self._get_character_line(character) for character in characters]))
        value = f'{self._role_emoji(role)} **{role.name.capitalize()}** ({len(characters)}):\n{player_lines}'
        return self._field(value)

    def _get_character_line(self, character: Character) -> str:
        signup_choice = character.signup_status
        signup_choice_indicator = '' if signup_choice == SignupStatus.ACCEPT else self._signup_choice_emoji(signup_choice)
        return f'{self._role_class_emoji(character)} {character.name} {signup_choice_indicator}'


def signed_and_not_declined_count(characters: List[Character]) -> int:
    return sum(1 for player in characters if player.signup_status != SignupStatus.DECLINE and player.roster_status != RosterStatus.DECLINE)


def roster_accepted_count(characters: List[Character]) -> int:
    return sum(1 for player in characters if player.roster_status == RosterStatus.ACCEPT)
