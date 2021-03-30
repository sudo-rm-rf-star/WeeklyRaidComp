from .RaidEventHandler import RaidEventHandler
from .RaidEventCreated import RaidEventCreated
from dokbot.entities.RaidMessage import RaidMessage
from dokbot.entities.RaidNotification import RaidNotification


class RaidEventCreatedHandler(RaidEventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def process(self, event: RaidEventCreated):
        ctx = await self.get_context(event)
        await RaidMessage.send_for_raiders(ctx=ctx)
        await RaidMessage.send_for_raid_leaders(ctx=ctx)
        await RaidNotification.send_messages(ctx)
