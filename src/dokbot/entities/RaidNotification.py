import discord

from dokbot.RaidContext import RaidContext
from dokbot.interactions.EmojiInteractionMessage import EmojiInteractionMessage
from persistence.MessagesResource import MessagesResource
from persistence.RaidEventsResource import RaidEventsResource
from persistence.PlayersResource import PlayersResource
from typing import List
from logic.enums.SignupStatus import SignupStatus


class RaidNotification(EmojiInteractionMessage):
    def __init__(self, ctx: RaidContext):
        content = f"You have been invited for {ctx.raid_event} organized by {ctx.raid_team}. " \
                  f"Please sign by clicking one of the reaction boxes."
        super(RaidNotification, self).__init__(ctx=ctx, content=content, reactions=SignupStatus.names())

    @classmethod
    async def send_to_team(cls, ctx: RaidContext) -> None:
        raider_ids = ctx.raid_team.raider_ids
        _add_invited_players_to_raid(ctx, raider_ids)
        for raider_id in raider_ids:
            if not ctx.raid_event.has_user_signed(raider_id):
                raider = await ctx.bot.fetch_user(raider_id)
                await cls._send(ctx, raider)

    @classmethod
    async def send_to_raider(cls, ctx: RaidContext, user: discord.User):
        await cls._send(ctx, user)

    @classmethod
    async def _send(cls, ctx: RaidContext, user: discord.User):
        _add_invited_players_to_raid(ctx, [user.id])
        msg = await cls(ctx).send_to(user)
        if msg:
            MessagesResource().create_personal_message(message_id=msg.id, guild_id=ctx.guild_id,
                                                       user_id=user.id, raid_name=ctx.raid_name,
                                                       raid_datetime=ctx.raid_datetime, team_name=ctx.team_name)


def _add_invited_players_to_raid(ctx: RaidContext, raider_ids: List[int]):
    # Get raiders
    raiders = []
    for raider_id in raider_ids:
        raider = PlayersResource().get_player_by_id(raider_id)
        if raider:
            raiders.append(raider)

    # Add raiders to event
    raid_event = RaidEventsResource(ctx).synced(ctx.raid_event)
    for raider in raiders:
        raid_event.add_to_signees(raider, SignupStatus.Unknown)
    RaidEventsResource(ctx).update_raid(raid_event)
