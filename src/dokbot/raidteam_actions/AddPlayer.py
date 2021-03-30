
def add_player(ctx: RaidTeamContext):
    member = FindPlayerInteraction(ctx=ctx)
    ctx.raid_team.raider_ids.append(member)
    RaidTeamsResource().update_raidteam(ctx.raid_team)

