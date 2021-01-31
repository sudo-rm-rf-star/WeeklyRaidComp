from logic.MessageRef import MessageRef
from typing import Dict, Any
from persistence.tables.DynamoDBTable import DynamoDBTable
from datetime import datetime


class MessagesTable(DynamoDBTable[MessageRef]):
    TABLE_NAME = 'messages'

    def __init__(self, ddb):
        super().__init__(ddb, MessagesTable.TABLE_NAME)

    def create_channel_message(self, message_id: int, guild_id: int, channel_id: int, raid_name: str, raid_datetime: datetime, group_id: int):
        message_ref = MessageRef(message_id=message_id, guild_id=guild_id, channel_id=channel_id, raid_name=raid_name,
                                 raid_datetime=raid_datetime, group_id=group_id)
        return self.create_message(message_ref)

    def create_personal_message(self, message_id: int, guild_id: int, user_id: int, raid_name: str, raid_datetime: datetime, group_id: int):
        message_ref = MessageRef(message_id=message_id, guild_id=guild_id, user_id=user_id, raid_name=raid_name,
                                 raid_datetime=raid_datetime, group_id=group_id)
        return self.create_message(message_ref)

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
