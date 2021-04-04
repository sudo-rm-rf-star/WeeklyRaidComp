from dokbot.RaidContext import RaidContext
from persistence.RaidEventsResource import RaidEventsResource


async def remove_raid(ctx: RaidContext):
    RaidEventsResource(ctx).remove_raid(ctx.raid_event)
