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
    def __init__(self):
        load_dotenv()
        access_key = os.getenv('AWS_ACCESS_KEY')
        secret_key = os.getenv('AWS_SECRET_KEY')
        sqs = boto3.resource('sqs', region_name='eu-west-1', aws_access_key_id=access_key,
                             aws_secret_access_key=secret_key)
        try:
            self.bot_queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
        except Exception:
            self.bot_queue = None
            print("# Queues are not supported yet. Make one through the console first with name: " + QUEUE_NAME)

    def send_event(self, event: Event, ctx: DokBotContext = None):
        if ctx:
            # We don't actually need to send events if we are already within the bot
            process(ctx, event)
        else:
            if self.bot_queue is None:
                print("Cannot send an outgoing message.")
                return

            Log.info(f"Sending event {event}")
            self.bot_queue.send_message(MessageBody=str({"event": event.to_message()}))

    async def listen(self, event_handler_factory: EventHandlerFactory):
        if self.bot_queue is None:
            print("Cannot listen to incoming messages.")
            return

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
