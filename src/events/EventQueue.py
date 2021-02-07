from dotenv import load_dotenv
from utils.Singleton import Singleton
import os
import boto3
import utils.Logger as Log
from .Event import Event
from .EventHandlerFactory import EventHandlerFactory

QUEUE_NAME = 'BotEventQueue'
QUEUE_POLLING_PERIOD_SECS = 5


class EventQueue(metaclass=Singleton):
    def __init__(self):
        load_dotenv()
        access_key = os.getenv('AWS_ACCESS_KEY')
        secret_key = os.getenv('AWS_SECRET_KEY')
        sqs = boto3.resource('sqs', region_name='eu-west-1', aws_access_key_id=access_key,
                             aws_secret_access_key=secret_key)
        self.bot_queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)

    def send_event(self, event: Event):
        Log.info(f"Sending event {event}")
        self.bot_queue.send_message(MessageBody=str({"event": event.to_message()}))

    async def listen(self, event_handler_factory: EventHandlerFactory):
        messages = self.bot_queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=QUEUE_POLLING_PERIOD_SECS)
        for message in messages:
            event = Event.from_message(eval(message.body)["event"])
            Log.info(f"Received event {event}")
            event_handler = event_handler_factory.create_event_handler(event)
            try:
                await event_handler.process(event)
            except Exception as e:
                await event_handler.process_failed(e, event)
            finally:
                if message:
                    message.delete()
