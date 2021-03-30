from dokbot.RaidTeamContext import RaidTeamContext
from dokbot.entities.RaidTeamMessage import RaidTeamMessage


async def switch_raidteam(ctx: RaidTeamContext):
    await RaidTeamMessage.reply_in_channel(ctx)
