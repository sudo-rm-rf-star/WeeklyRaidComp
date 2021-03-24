from utils.EmojiNames import SIGNUP_STATUS_EMOJI
from logic.RaidEvent import RaidEvent
from dokbot.interactions.EmojiInteractionMessage import EmojiInteractionMessage
import discord
from logic.RaidTeam import RaidTeam
from dokbot.commands.raid.RaidContext import RaidContext


class RaidNotification(EmojiInteractionMessage):
    def __init__(self, ctx: RaidContext):
        content = f"You have been invited for {ctx.raid_event} for {ctx.raidteam}. " \
                  f"Please sign by clicking one of the reaction boxes."
        emojis = SIGNUP_STATUS_EMOJI.values()
        super(RaidNotification, self).__init__(ctx=ctx, content=content, reactions=emojis)

    @staticmethod
    async def send_messages(ctx: RaidContext) -> None:
        for raider in raiders:
            if not raid_event.has_user_signed(raider.id) or len(raiders) == 1:
                msg = await RaidNotification(self.client, self.discord_guild, raid_event, raid_team).send_to(raider)
                if msg:
                    self.messages_resource.create_personal_message(message_id=msg.id, guild_id=self.discord_guild.id,
                                                                   user_id=raider.id, raid_name=raid_event.name,
                                                                   raid_datetime=raid_event.datetime,
                                                                   team_name=raid_event.team_name)
