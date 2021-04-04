from .RaidEventHandler import RaidEventHandler
from .RaidEventRemoved import RaidEventRemoved
from datetime import datetime
from persistence.RaidEventsResource import RaidEventsResource


class RaidEventRemovedHandler(RaidEventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def process(self, event: RaidEventRemoved):
        ctx = await self.get_context(event)

        for message_ref in ctx.raid_event.message_refs:
            message = await ctx.bot.message(channel_id=message_ref.channel_id, message_id=message_ref.message_id)
            if message:
                await message.delete()

        if ctx.raid_event.in_future():
            msg = f'{ctx.raid_event} has been cancelled.'
            raiders = ctx.raid_event.get_characters()
            await ctx.send_to_raiders(raiders, msg)

        RaidEventsResource(ctx).delete_raid(raid_event=ctx.raid_event)
