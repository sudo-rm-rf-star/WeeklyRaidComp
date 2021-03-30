from exceptions.MissingImplementationException import MissingImplementationException
from .Event import Event
from utils.Constants import MAINTAINER_ID
import utils.Logger as Log
import traceback
from dokbot.DokBot import DokBot


class EventHandler:
    def __init__(self, bot: DokBot):
        self.bot = bot

    async def process(self, event: Event):
        raise MissingImplementationException(self)

    async def process_failed(self, exception: Exception, event: Event):
        Log.error(f"Failed to process {event} because of {exception}\n{traceback.format_exc()}")
        maintainer = await self.bot.fetch_user(MAINTAINER_ID)
        await maintainer.send(f"Failed to process {event}")