from logic.RaidEvent import RaidEvent
from typing import Optional, Dict, Any, List
from persistence.DynamoDBTable import DynamoDBTable
from utils.DateOptionalTime import DateOptionalTime
from boto3.dynamodb.conditions import Attr
from client.entities.DiscordMessageIdentifier import DiscordMessageIdentifier


class RaidEventsTable(DynamoDBTable[RaidEvent]):
    TABLE_NAME = 'raid_events'
    INDEX_NAME = 'discord_id_index'

    def __init__(self, ddb):
        super().__init__(ddb, RaidEventsTable.TABLE_NAME)

    def get_raid_event(self, raid_name: str, raid_datetime: DateOptionalTime) -> Optional[RaidEvent]:
        return super(RaidEventsTable, self).get_item(name=raid_name, timestamp=raid_datetime.to_timestamp())

    def get_raid_event_by_message_id(self, message_id: DiscordMessageIdentifier, is_notification: bool) -> Optional[RaidEvent]:
        attr_name = 'notification_ids' if is_notification else 'message_ids'
        return self.to_unique_object(self.table.scan(FilterExpression=Attr(attr_name).contains(message_id.to_str())))

    def list_raid_events(self) -> List[RaidEvent]:
        return self.scan()

    def put_raid_event(self, raid_event: RaidEvent) -> None:
        return super(RaidEventsTable, self).put_item(raid_event)

    def remove_raid_event(self, raid_name: str, raid_datetime: DateOptionalTime) -> bool:
        return super(RaidEventsTable, self).remove_item(name=raid_name, timestamp=raid_datetime.to_timestamp())

    def _to_object(self, item: Dict[str, Any]) -> RaidEvent:
        return RaidEvent.from_dict(item)

    def _to_item(self, raid_event: RaidEvent) -> Dict[str, Any]:
        return raid_event.to_dict()

    def _table_kwargs(self):
        return {
            'KeySchema': [
                {
                    'AttributeName': 'timestamp',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'name',
                    'KeyType': 'RANGE'
                }
            ],
            'AttributeDefinitions': [
                {
                    'AttributeName': 'name',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'timestamp',
                    'AttributeType': 'N'
                }
            ],
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        }
