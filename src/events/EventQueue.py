from dotenv import load_dotenv
from utils.Singleton import Singleton
import os
import boto3
import utils.Logger as Log
from .EventHandler import EventHandler
from .Event import Event
from .EventHandlerFactory import EventHandlerFactory
from dokbot.DokBotContext import DokBotContext
import asyncio

QUEUE_NAME = 'BotEventQueue'
QUEUE_POLLING_PERIOD_SECS = 5


class EventQueue(metaclass=Singleton):
    def __init__(self, ctx: DokBotContext = None):
        load_dotenv()
        access_key = os.getenv('AWS_ACCESS_KEY')
        secret_key = os.getenv('AWS_SECRET_KEY')
        sqs = boto3.resource('sqs', region_name='eu-west-1', aws_access_key_id=access_key,
                             aws_secret_access_key=secret_key)
        self.bot_queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
        self.ctx = ctx

    def send_event(self, event: Event):
        Log.info(f"Sending event {event}")
        if self.ctx:
            # We don't actually need to send events if we are already within the bot
            process(self.ctx, event)
        else:
            self.bot_queue.send_message(MessageBody=str({"event": event.to_message()}))

    async def listen(self, event_handler_factory: EventHandlerFactory):
        messages = self.bot_queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=QUEUE_POLLING_PERIOD_SECS)
        for message in messages:
            event = Event.from_message(eval(message.body)["event"])
            Log.info(f"Received event {event}")
            event_handler = await event_handler_factory.create_event_handler(event)
            await process_now(event_handler, event)
            if message:
                message.delete()


async def process_now(event_handler: EventHandler, event: Event):
    try:
        await event_handler.process(event)
    except Exception as e:
        await event_handler.process_failed(e, event)


async def _process(ctx: DokBotContext, event: Event):
    event_handler = await EventHandlerFactory(ctx.bot).create_event_handler(event)
    await process_now(event_handler, event)


def process(ctx: DokBotContext, event: Event):
    asyncio.create_task(_process(ctx, event))
