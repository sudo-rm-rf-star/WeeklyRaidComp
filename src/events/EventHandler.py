from src.events.SQSQueue import SQSQueue

if __name__ == '__main__':
    SQSQueue().send_message({'msg': 'HEy'})
