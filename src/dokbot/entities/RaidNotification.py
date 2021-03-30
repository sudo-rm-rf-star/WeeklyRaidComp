from utils.EmojiNames import SIGNUP_STATUS_EMOJI
from dokbot.interactions.EmojiInteractionMessage import EmojiInteractionMessage
from dokbot.RaidContext import RaidContext
from persistence.MessagesResource import MessagesResource


class RaidNotification(EmojiInteractionMessage):
    def __init__(self, ctx: RaidContext):
        content = f"You have been invited for {ctx.raid_event} for {ctx.raidteam}. " \
                  f"Please sign by clicking one of the reaction boxes."
        emojis = SIGNUP_STATUS_EMOJI.values()
        super(RaidNotification, self).__init__(ctx=ctx, content=content, reactions=emojis)

    @staticmethod
    async def send_messages(ctx: RaidContext) -> None:
        for raider_id in ctx.raid_team.raider_ids:
            if not ctx.raid_event.has_user_signed(raider_id):
                raider = await ctx.bot.fetch_user(raider_id)
                msg = await RaidNotification(ctx).send_to(raider)
                if msg:
                    MessagesResource().create_personal_message(message_id=msg.id, guild_id=ctx.guild_id,
                                                               user_id=raider_id, raid_name=ctx.raid_name,
                                                               raid_datetime=ctx.raid_datetime, team_name=ctx.team_name)
