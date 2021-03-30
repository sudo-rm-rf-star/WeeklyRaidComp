from persistence.RaidTeamsResource import RaidTeamsResource
from dokbot.RaidTeamContext import RaidTeamContext
from dokbot.interactions.FindMemberInteraction import FindMemberInteraction


async def add_raidleader(ctx: RaidTeamContext):
    member = await FindMemberInteraction.interact(ctx)
    ctx.raid_team.manager_ids.append(member.id)
    RaidTeamsResource().update_raidteam(ctx.raid_team)
