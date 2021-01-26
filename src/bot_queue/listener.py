from src.bot_queue.SQSQueue import SQSQueue

if __name__ == '__main__':
    sqs_queue = SQSQueue()
    sqs_queue.listen(lambda msg: print(msg.items()))
