from dokbot.RaidTeamContext import RaidTeamContext
from dokbot.interactions.OptionInteraction import OptionInteraction
from persistence.RaidTeamsResource import RaidTeamsResource


async def add_raiders(ctx: RaidTeamContext):
    roles = await ctx.guild.fetch_roles()
    content = "Please select a role. All of the people who have this role get added to the raid team"
    options = [role.name for role in roles]
    role_name = await OptionInteraction.interact(ctx=ctx, options=options, content=content)
    role = [role for role in roles if role.name == role_name]
    if len(role) != 1:
        await ctx.reply(f"{role_name} is not a valid role.")
        return
    role = role[0]
    members = await ctx.guild.fetch_members(limit=None).flatten()
    new_raider_ids = [member.id for member in members if member.id not in ctx.raid_team.raider_ids and role in member.roles]
    for member in members:
        if member.id not in ctx.raid_team.raider_ids and role in member.roles:
            ctx.raid_team.raider_ids.append(member.id)
            await member.send(f'You have been added to {ctx.raid_team}')
    RaidTeamsResource().update_raidteam(ctx.raid_team)
    await ctx.reply(f"Added {len(new_raider_ids)} raider(s) to the to raid team.")
