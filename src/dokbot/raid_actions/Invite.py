from dokbot.RaidContext import RaidContext
from dokbot.interactions.FindMemberInteraction import FindMemberInteraction
from dokbot.entities.RaidNotification import RaidNotification


async def invite(ctx: RaidContext):
    member = await FindMemberInteraction.interact(ctx)
    await RaidNotification.send_to_raider(ctx, member)
    await ctx.reply(f'Invited {member.display_name} to {ctx.raid_event}')
