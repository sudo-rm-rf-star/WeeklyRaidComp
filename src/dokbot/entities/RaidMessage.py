from typing import List, Optional, Dict

from dokbot.utils.DiscordUtils import get_emoji
from dokbot.utils.DiscordUtils import get_message
from dokbot.RaidContext import RaidContext
from dokbot.entities.DiscordMessage import DiscordMessage, field
from dokbot.raid_actions.ActionsRaid import ActionsRaid
from logic.Character import Character
from logic.RaidEvent import RaidEvent
from logic.enums.RosterStatus import RosterStatus
from logic.enums.SignupStatus import SignupStatus
from persistence.MessagesResource import MessagesResource
from persistence.RaidEventsResource import RaidEventsResource
from utils.Constants import DATETIMESEC_FORMAT
from utils.EmojiNames import CALENDAR_EMOJI, CLOCK_EMOJI
from utils.EmojiNames import SIGNUP_STATUS_EMOJI
from exceptions.InternalBotException import InternalBotException
import discord


class RaidMessage(DiscordMessage):
    def __init__(self, ctx: RaidContext, for_raid_leaders: bool, embed: discord.Embed = None):
        super().__init__(ctx=ctx, embed=embed, reactions=_get_emoji_names(ctx, for_raid_leaders))

    @classmethod
    async def get_embed(cls, ctx: RaidContext, **kwargs) -> Optional[discord.Embed]:
        for_raid_leaders = kwargs['for_raid_leaders']
        embed = {'title': _get_title(raid_event=ctx.raid_event),
                 'description': await _get_description(ctx=ctx),
                 'fields': await _get_fields(ctx=ctx, for_raid_leaders=for_raid_leaders),
                 'footer': get_footer(raid_event=ctx.raid_event, for_raid_leaders=for_raid_leaders),
                 'color': 2171428,
                 'type': 'rich'}
        return discord.Embed.from_dict(embed)

    @classmethod
    async def send(cls, ctx: RaidContext, recipient, **kwargs):
        msg = await super(RaidMessage, cls).send(ctx=ctx, recipient=recipient, **kwargs)
        if len(msg) != 1:
            raise InternalBotException("Unhandled case")
        msg = msg[0]
        raid_event = ctx.raid_event
        message_ref = MessagesResource().create_channel_message(message_id=msg.id, guild_id=ctx.guild_id,
                                                                channel_id=msg.channel.id, raid_name=raid_event.name,
                                                                raid_datetime=raid_event.datetime,
                                                                team_name=raid_event.team_name, **kwargs)
        raid_event.message_refs.append(message_ref)
        RaidEventsResource().update_raid(raid_event)

    @classmethod
    async def send_for_raiders(cls, ctx: RaidContext, **kwargs):
        recipient = await ctx.get_events_channel()
        await cls.send(ctx=ctx, recipient=recipient, for_raid_leaders=False, **kwargs)

    @classmethod
    async def send_for_raid_leaders(cls, ctx: RaidContext, **kwargs):
        recipient = await ctx.get_managers_channel()
        await cls.send(ctx=ctx, recipient=recipient, for_raid_leaders=True, **kwargs)

    @staticmethod
    async def update_messages(ctx: RaidContext):
        for message_ref in ctx.raid_event.message_refs:
            discord_message = await get_message(ctx.guild, message_ref)
            raid_message = await RaidMessage.make(ctx=ctx, **message_ref.kwargs)
            await raid_message.update(discord_message)


def _get_title(raid_event: RaidEvent) -> str:
    return f'{raid_event.get_name()}'


async def _get_description(ctx: RaidContext) -> str:
    return f'{await get_emoji(ctx.bot, CALENDAR_EMOJI)} {ctx.raid_event.get_date()} ({ctx.raid_event.get_weekday().capitalize()})\n' \
           f'{await get_emoji(ctx.bot, CLOCK_EMOJI)} {ctx.raid_event.get_time()}\n'


def get_footer(raid_event: RaidEvent, for_raid_leaders: bool) -> Optional[Dict[str, str]]:
    if for_raid_leaders:
        text = f"Generate this message again by typing: >raid {raid_event.get_name()} {raid_event.get_datetime()}"
    else:
        text = f'Created at: {raid_event.created_at.strftime(DATETIMESEC_FORMAT)}. Last updated at: {raid_event.updated_at.strftime(DATETIMESEC_FORMAT)}'

    return {'text': text}


async def _get_fields(ctx: RaidContext, for_raid_leaders: bool) -> List[Dict[str, str]]:
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

    fields.extend(await _get_control_fields(ctx, for_raid_leaders=for_raid_leaders))
    return fields


def _get_title_for_roster_status(characters: List[Character], roster_status: RosterStatus):
    title = {
        RosterStatus.ACCEPT: "Raid Team",
        RosterStatus.EXTRA: "Standby",
        RosterStatus.DECLINE: "Declined",
        RosterStatus.UNDECIDED: "Signees"
    }
    return field(f"**__{title[roster_status]}__** ({len(characters)})", inline=False)


async def _get_control_fields(ctx: RaidContext, for_raid_leaders: bool):
    fields = []
    if for_raid_leaders:
        for action in ActionsRaid:
            emoji = await ctx.bot.emoji(action.name)
            entry = "{0} {1}".format(emoji, action.value)
            fields.append(field(entry, inline=False))
    return fields


def _get_emoji_names(ctx: RaidContext, for_raid_leaders: bool):
    if for_raid_leaders:
        return [action.name for action in ActionsRaid]
    elif ctx.raid_event.is_open:
        return SIGNUP_STATUS_EMOJI.values()
    else:
        return []