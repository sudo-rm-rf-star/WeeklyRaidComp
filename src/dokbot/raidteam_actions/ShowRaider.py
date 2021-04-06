from dokbot.RaidTeamContext import RaidTeamContext
from dokbot.entities.ShowPlayerMessage import ShowPlayerMessage
from dokbot.interactions.FindPlayerInteraction import FindPlayerInteraction


async def show_raider(ctx: RaidTeamContext):
    player = await FindPlayerInteraction.interact(ctx)
    member = await ctx.guild.fetch_member(player.discord_id)
    await ShowPlayerMessage.reply_in_channel(ctx=ctx, player=player, member=member)
