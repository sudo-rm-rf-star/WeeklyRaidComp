from persistence.RaidTeamsResource import RaidTeamsResource
from dokbot.RaidTeamContext import RaidTeamContext
from dokbot.interactions.FindMemberInteraction import FindMemberInteraction


async def add_raider(ctx: RaidTeamContext):
    member = await FindMemberInteraction.interact(ctx)
    ctx.raid_team.raider_ids.append(member.id)
    RaidTeamsResource().update_raidteam(ctx.raid_team)
