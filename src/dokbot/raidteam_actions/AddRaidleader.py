from persistence.RaidTeamsResource import RaidTeamsResource
from dokbot.RaidTeamContext import RaidTeamContext
from dokbot.interactions.FindMemberInteraction import FindMemberInteraction


async def add_raid_leader(ctx: RaidTeamContext):
    member = await FindMemberInteraction.interact(ctx)
    if member.id in ctx.raid_team.manager_ids:
        await ctx.reply(f"{member} is already manager of the raid team.")
        return
    ctx.raid_team.manager_ids.append(member.id)
    RaidTeamsResource().update_raidteam(ctx.raid_team)
    await ctx.reply(f"Added {member} as manager for the raid team.")
