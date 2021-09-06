from dokbot.RaidContext import RaidContext
from dokbot.interactions.FindPlayerInteraction import FindPlayerInteraction
from logic.enums.RosterStatus import RosterStatus
from persistence.RaidEventsResource import RaidEventsResource


async def update_roster(ctx: RaidContext, status: RosterStatus):
    player = await FindPlayerInteraction.interact(ctx)
    RaidEventsResource(ctx).update_roster(ctx.raid_event, {
        player.discord_id: (status.name, 0)
    })
    await ctx.reply(f'Raid event for {ctx.raid_event.get_name()} on {ctx.raid_event.get_datetime()} has been successfully updated.')
