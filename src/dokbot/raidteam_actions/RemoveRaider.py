from persistence.RaidTeamsResource import RaidTeamsResource
from dokbot.RaidTeamContext import RaidTeamContext
from dokbot.interactions.FindMemberInteraction import FindMemberInteraction


async def remove_raider(ctx: RaidTeamContext):
    member = await FindMemberInteraction.interact(ctx)
    if member.id not in ctx.raid_team.raider_ids:
        await ctx.reply(f"{member} is not yet in the raid team.")
        return
    ctx.raid_team.raider_ids.remove(member.id)
    RaidTeamsResource().update_raidteam(ctx.raid_team)
    await ctx.reply(f"Removed {member} from raid team.")
