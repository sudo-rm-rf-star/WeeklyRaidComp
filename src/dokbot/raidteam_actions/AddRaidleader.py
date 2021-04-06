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
    await member.send(f'You are now a raid leader for {ctx.raid_team}.\n'
                      f'You can start managing the raidteam and its raids by typing !dokbot in the channel #{await ctx.get_managers_channel()}')
