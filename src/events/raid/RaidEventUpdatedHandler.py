from .RaidEventHandler import RaidEventHandler
from .RaidEventUpdated import RaidEventUpdated
from dokbot.entities.RaidMessage import RaidMessage


class RaidEventUpdatedHandler(RaidEventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def process(self, event: RaidEventUpdated):
        ctx = await self.get_context(event)
        await RaidMessage.update_messages(ctx=ctx)
