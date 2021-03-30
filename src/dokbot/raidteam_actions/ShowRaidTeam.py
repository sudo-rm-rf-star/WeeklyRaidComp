from dokbot.RaidTeamContext import RaidTeamContext
from dokbot.entities.ShowRaidTeamMessage import ShowRaidTeamMessage


async def show_raid_team(ctx: RaidTeamContext):
    await ShowRaidTeamMessage.reply_in_channel(ctx)
