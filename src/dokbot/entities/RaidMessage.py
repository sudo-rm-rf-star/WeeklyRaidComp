import asyncio
from typing import List, Optional, Dict, Union

import discord
from discord import Embed

from dokbot.entities.DiscordMessage import DiscordMessage, field
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
from dokbot.commands.raid.RaidContext import RaidContext
from persistence.MessagesResource import MessagesResource
from logic.MessageRef import MessageRef


class RaidMessage(DiscordMessage):
    def __init__(self, ctx: RaidContext, embed: discord.Embed = None):
        super().__init__(ctx=ctx, embed=embed, reactions=[action.name for action in RaidControlAction])

    @staticmethod
    async def create_message(ctx: RaidContext):
        embed = await raid_to_embed(ctx=ctx)
        return RaidMessage(ctx=ctx, embed=embed)

    @staticmethod
    async def send_message(ctx: RaidContext, recipient=None):
        if not recipient:
            recipient = await ctx.get_events_channel()
        msg = await (await RaidMessage.create_message(ctx=ctx)).send_to(recipient)

        raid_event = ctx.raid_event
        message_ref = MessageRef(message_id=msg.id, guild_id=ctx.guild_id, channel_id=recipient.id,
                                 raid_name=raid_event.name, raid_datetime=raid_event.datetime,
                                 team_name=raid_event.name)
        MessagesResource().create_channel_message(message_id=msg.id, guild_id=ctx.guild_id,
                                                  channel_id=msg.channel.id, raid_name=raid_event.name,
                                                  raid_datetime=raid_event.datetime, team_name=raid_event.name)
        raid_event.message_refs.append(message_ref)
        return msg

    @staticmethod
    async def sync_message(ctx: RaidContext):
        raid_msg = await RaidMessage.create_message(ctx=ctx)
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
        for message_ref in self.ctx.raid_event.message_refs:
            message = await self._update_message(message_ref)
            if message:
                await self.add_reactions(message)

    async def add_reactions(self, message: discord.Message) -> None:
        try:
            if not self.ctx.raid_event.is_open:
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


async def raid_to_embed(ctx: RaidContext) -> Embed:
    embed = {'title': _get_title(raid_event=ctx.raid_event),
             'description': await _get_description(ctx=ctx),
             'fields': await _get_fields(ctx=ctx),
             'footer': get_footer(raid_event=ctx.raid_event),
             'color': 2171428,
             'type': 'rich'}
    return Embed.from_dict(embed)


def _get_title(raid_event: RaidEvent) -> str:
    return f'{raid_event.get_name()}'


async def _get_description(ctx: RaidContext) -> str:
    return f'{await get_emoji(ctx.bot, CALENDAR_EMOJI)} {ctx.raid_event.get_date()} ({ctx.raid_event.get_weekday().capitalize()})\n' \
           f'{await get_emoji(ctx.bot, CLOCK_EMOJI)} {ctx.raid_event.get_time()}\n'


def get_footer(raid_event: RaidEvent) -> Optional[Dict[str, str]]:
    return {'text': f'Created at: {raid_event.created_at.strftime(DATETIMESEC_FORMAT)}. ' +
                    f'Last updated at: {raid_event.updated_at.strftime(DATETIMESEC_FORMAT)}'}


async def _get_fields(ctx: RaidContext) -> List[Dict[str, str]]:
    raid_team = ctx.raid_event.roster.get_team()
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


async def _get_control_fields(ctx: RaidContext):
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
