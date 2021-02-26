import asyncio
from typing import List, Optional, Dict, Union

import discord
from discord import Embed

from dokbot.entities.DiscordMessage import DiscordMessage, field, empty_field
from exceptions.InternalBotException import InternalBotException
from logic.Character import Character
from logic.RaidEvent import RaidEvent
from logic.enums.RosterStatus import RosterStatus
from logic.enums.SignupStatus import SignupStatus
from utils.Constants import DATETIMESEC_FORMAT
from utils.EmojiNames import CALENDAR_EMOJI, CLOCK_EMOJI
from utils.EmojiNames import SIGNUP_STATUS_EMOJI
from dokbot.DiscordUtils import get_emoji
from dokbot.entities.enums.RaidControlAction import RaidControlAction
from dokbot.DokBotContext import DokBotContext


class RaidMessage(DiscordMessage):
    def __init__(self, ctx: DokBotContext, raid_event: RaidEvent, embed: discord.Embed = None):
        self.raid_event = raid_event
        super().__init__(ctx=ctx, embed=embed, reactions=[action.name for action in RaidControlAction])

    @staticmethod
    async def create_message(ctx: DokBotContext, raid_event: RaidEvent):
        embed = await raid_to_embed(ctx=ctx, raid_event=raid_event)
        return RaidMessage(ctx=ctx, raid_event=raid_event, embed=embed)

    @staticmethod
    async def send_message(ctx: DokBotContext, raid_event: RaidEvent, recipient):
        raid_msg = await RaidMessage.create_message(ctx=ctx, raid_event=raid_event)
        return await raid_msg.send_to(recipient)

    @staticmethod
    async def sync_message(ctx: DokBotContext, raid_event: RaidEvent):
        raid_msg = await RaidMessage.create_message(ctx=ctx, raid_event=raid_event)
        return raid_msg.sync()

    async def send_to(self, recipient: Union[discord.User, discord.TextChannel]) -> discord.Message:
        msgs = await super(RaidMessage, self).send_to(recipient)
        if len(msgs) > 1:
            raise InternalBotException("Unhandled case")
        await self.add_reactions(msgs[0])
        return msgs[0]

    def sync(self):
        asyncio.create_task(self._sync())

    async def _sync(self):
        """Updates the existing RaidMessages"""
        for message_ref in self.raid_event.message_refs:
            message = await self._update_message(message_ref)
            if message:
                await self.add_reactions(message)

    async def add_reactions(self, message: discord.Message) -> None:
        try:
            if not self.raid_event.is_open:
                await message.clear_reactions()
            else:
                emojis = [await self.ctx.bot.get_emoji(emoji_name) for status, emoji_name in SIGNUP_STATUS_EMOJI.items()
                          if status != SignupStatus.UNDECIDED]
                if set(emojis) != set(reaction.emoji for reaction in message.reactions):
                    await message.clear_reactions()
                    for emoji in emojis:
                        await message.add_reaction(emoji=emoji)
        except discord.Forbidden:  # This is not possible in DM
            pass


async def raid_to_embed(ctx: DokBotContext, raid_event: RaidEvent) -> Embed:
    embed = {'title': _get_title(raid_event=raid_event),
             'description': await _get_description(ctx=ctx, raid_event=raid_event),
             'fields': await _get_fields(ctx=ctx, raid_event=raid_event),
             'footer': get_footer(raid_event=raid_event),
             'color': 2171428,
             'type': 'rich'}
    return Embed.from_dict(embed)


def _get_title(raid_event: RaidEvent) -> str:
    return f'{raid_event.get_name()}'


async def _get_description(client: discord.Client, raid_event: RaidEvent) -> str:
    return f'{await get_emoji(client, CALENDAR_EMOJI)} {raid_event.get_date()} ({raid_event.get_weekday().capitalize()})\n' \
           f'{await get_emoji(client, CLOCK_EMOJI)} {raid_event.get_time()}\n'


def get_footer(raid_event: RaidEvent) -> Optional[Dict[str, str]]:
    return {'text': f'Created at: {raid_event.created_at.strftime(DATETIMESEC_FORMAT)}. ' +
                    f'Last updated at: {raid_event.updated_at.strftime(DATETIMESEC_FORMAT)}'}


async def _get_fields(ctx: DokBotContext, raid_event: RaidEvent) -> List[Dict[str, str]]:
    raid_team = raid_event.roster.get_team()
    characters_by_status = {roster_status: [] for roster_status in RosterStatus}
    for character in raid_team:
        characters_by_status[character.get_roster_status()].append(character)

    fields = []
    for roster_status in [RosterStatus.ACCEPT, RosterStatus.UNDECIDED, RosterStatus.EXTRA]:
        characters = [char for char in characters_by_status[roster_status] if not (
                    char.get_roster_status() == RosterStatus.UNDECIDED and char.get_signup_status() == SignupStatus.UNDECIDED)]
        if len(characters) > 0:
            fields.append(_get_title_for_roster_status(characters, roster_status))
            fields.extend(await DiscordMessage.show_characters(ctx=ctx, characters=characters))

    declined_characters = [char.name for char in characters_by_status[RosterStatus.DECLINE]]
    invited_but_not_signed_characters = [char.name for char in characters_by_status[RosterStatus.UNDECIDED]
                                         if char.get_signup_status() == SignupStatus.UNDECIDED]
    if len(invited_but_not_signed_characters) > 20:
        value = f'**Invited**: {", ".join(invited_but_not_signed_characters[:20])}, ...'
        fields.append(field(value, inline=False))
    elif len(invited_but_not_signed_characters) > 0:
        value = f'**Invited**: {", ".join(invited_but_not_signed_characters)}'
        fields.append(field(value, inline=False))
    if len(declined_characters) > 0:
        value = f'**Declined**: {", ".join(declined_characters)}'
        fields.append(field(value, inline=False))

    fields.extend(await _get_control_fields(ctx))
    return fields


async def _get_control_fields(ctx: DokBotContext):
    fields = []
    for action in RaidControlAction:
        emoji = await ctx.bot.emoji(action.name)
        entry = "{0} {1}".format(emoji, action.value)
        fields.append(field(entry))
    return fields


def _get_title_for_roster_status(characters: List[Character], roster_status: RosterStatus):
    title = {
        RosterStatus.ACCEPT: "Raid Team",
        RosterStatus.EXTRA: "Standby",
        RosterStatus.DECLINE: "Declined",
        RosterStatus.UNDECIDED: "Signees"
    }
    return field(f"**__{title[roster_status]}__** ({len(characters)})", inline=False)
