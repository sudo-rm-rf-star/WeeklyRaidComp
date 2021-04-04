from dokbot.RaidContext import RaidContext
from persistence.RaidEventsResource import RaidEventsResource


async def open_raid(ctx: RaidContext):
    ctx.raid_event.is_open = True
    RaidEventsResource(ctx).update_raid(ctx.raid_event)
    await ctx.reply(f"Opened {ctx.raid_event} so anyone can sign.")
