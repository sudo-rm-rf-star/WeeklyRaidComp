from dokbot.RaidContext import RaidContext
from dokbot.interactions.FindPlayerInteraction import FindPlayerInteraction
from logic.enums.RosterStatus import RosterStatus
from persistence.RaidEventsResource import RaidEventsResource
from .PublishRosterChanges import publish_roster_changes


async def update_roster(ctx: RaidContext, status: RosterStatus):
    player = await FindPlayerInteraction.interact(ctx)
    updated_character = ctx.raid_event.add_to_roster(player, status)
    RaidEventsResource().update_raid(ctx.raid_event)
    publish_roster_changes(ctx=ctx, characters=[updated_character])
    await ctx.reply(f'Raid event for {ctx.raid_event.get_name()} on {ctx.raid_event.get_datetime()} has been successfully updated.')
