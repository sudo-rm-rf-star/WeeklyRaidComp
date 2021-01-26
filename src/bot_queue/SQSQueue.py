from dotenv import load_dotenv
import os
import boto3
from typing import Dict, Callable

QUEUE_NAME = 'BotEventQueue'
QUEUE_POLLING_PERIOD_SECS = 5


class SQSQueue:
    def __init__(self):
        load_dotenv()
        access_key = os.getenv('AWS_ACCESS_KEY')
        secret_key = os.getenv('AWS_SECRET_KEY')
        sqs = boto3.resource('sqs', region_name='eu-west-1', aws_access_key_id=access_key,
                             aws_secret_access_key=secret_key)
        self.bot_queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)

    def send_message(self, msg: Dict):
        self.bot_queue.send_message(MessageBody=str(msg))

    def listen(self, handle_message: Callable):
        while 1:
            messages = self.bot_queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=QUEUE_POLLING_PERIOD_SECS)
            for message in messages:
                body = message.body
                handle_message(eval(body))
                message.delete()
