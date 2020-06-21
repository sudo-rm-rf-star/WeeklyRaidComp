from logic.MessageRef import MessageRef
from typing import Dict, Any
from persistence.DynamoDBTable import DynamoDBTable


class MessagesTable(DynamoDBTable[MessageRef]):
    TABLE_NAME = 'messages'

    def __init__(self, ddb):
        super().__init__(ddb, MessagesTable.TABLE_NAME)

    def get_message(self, message_id: int) -> MessageRef:
        return super(MessagesTable, self).get_item(message_id=message_id)

    def create_message(self, message: MessageRef) -> None:
        return super(MessagesTable, self).put_item(message)

    def _to_object(self, item: Dict[str, Any]) -> MessageRef:
        return MessageRef.from_dict(item)

    def _to_item(self, message: MessageRef) -> Dict[str, Any]:
        return message.to_dict()

    def _to_key(self, message_id: int):
        return {'message_id': str(message_id)}

    def _table_kwargs(self):
        return {
            'KeySchema': [
                {
                    'AttributeName': 'message_id',
                    'KeyType': 'HASH'
                },
            ],
            'AttributeDefinitions': [
                {
                    'AttributeName': 'message_id',
                    'AttributeType': 'S'
                }
            ],
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 3,
                'WriteCapacityUnits': 3
            }
        }
