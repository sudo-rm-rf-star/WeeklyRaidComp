from persistence.RaidTeamsResource import RaidTeamsResource
from dokbot.RaidTeamContext import RaidTeamContext
from dokbot.interactions.FindMemberInteraction import FindMemberInteraction


async def add_raider(ctx: RaidTeamContext):
    member = await FindMemberInteraction.interact(ctx)
    if member.id in ctx.raid_team.raider_ids:
        await ctx.reply(f"{member} is already in the raid team.")
        return
    ctx.raid_team.raider_ids.append(member.id)
    RaidTeamsResource().update_raidteam(ctx.raid_team)
    await member.send(f'You have been added to {ctx.raid_team}')
    await ctx.reply(f"Added {member} to raid team.")
