from discord.ext.commands import Cog, Bot
from discord.ext.tasks import loop
from events.EventQueue import EventQueue
from events.EventHandlerFactory import EventHandlerFactory
from dokbot.DokBot import DokBot


class EventCog(Cog):
    def __init__(self, bot: DokBot):
        self.events_queue = EventQueue()
        self.events_handler_factory = EventHandlerFactory(bot)
        self.listen_for_events.start()

    @loop(seconds=10.0)
    async def listen_for_events(self):
        await self.events_queue.listen(self.events_handler_factory)

