from logic.RaidEvent import RaidEvent
from typing import Optional, Dict, Any, List
from persistence.DynamoDBTable import DynamoDBTable
from utils.DateOptionalTime import DateOptionalTime
from boto3.dynamodb.conditions import Attr, Key
from client.entities.DiscordMessageIdentifier import DiscordMessageIdentifier


class RaidEventsTable(DynamoDBTable[RaidEvent]):
    TABLE_NAME = 'raid_events'
    INDEX_NAME = 'guild_team_index'

    def __init__(self, ddb):
        super().__init__(ddb, RaidEventsTable.TABLE_NAME)

    def get_raid_event(self, guild_id: int, group_id: int, raid_name: str, raid_datetime: DateOptionalTime) -> Optional[RaidEvent]:
        return super(RaidEventsTable, self).get_item(guild_id=guild_id, group_id=group_id, name=raid_name, timestamp=raid_datetime)

    def get_raid_event_by_message_id(self, guild_id: int, message_id: DiscordMessageIdentifier, is_notification: bool) -> Optional[RaidEvent]:
        attr_name = 'notification_ids' if is_notification else 'message_ids'
        return self.to_unique_object(self.table.query(IndexName=RaidEventsTable.INDEX_NAME,
                                                      KeyConditionExpression=Key('guild_id').eq(guild_id),
                                                      FilterExpression=Attr(attr_name).contains(message_id.to_str())))

    def list_raid_events(self, guild_id: int, group_id: Optional[int]) -> List[RaidEvent]:
        return self.table.query(IndexName=RaidEventsTable.INDEX_NAME, KeyConditionExpression=Key('guild_id#group_id').eq(f'{guild_id}#{group_id}'))

    def put_raid_event(self, raid_event: RaidEvent) -> None:
        return super(RaidEventsTable, self).put_item(raid_event)

    def remove_raid_event(self, raid_name: str, raid_datetime: DateOptionalTime) -> bool:
        return super(RaidEventsTable, self).remove_item(name=raid_name, timestamp=raid_datetime.to_timestamp())

    def _to_object(self, item: Dict[str, Any]) -> RaidEvent:
        item['name'], item['timestamp'] = tuple(item['name#timestamp'].split('#'))
        item['guild_id'], item['group_id'] = tuple(item['guild_id#group_id'].split('#'))
        return RaidEvent.from_dict(item)

    def _to_item(self, raid_event: RaidEvent) -> Dict[str, Any]:
        item = raid_event.to_dict()
        item['name#timestamp'] = item['name'] + '#' + item['timestamp']
        item['guild_id#group_id'] = item['guild_id'] + '#' + item['group_id']
        return item

    def _to_key(self, guild_id: int, group_id: int, raid_name: str, raid_datetime: DateOptionalTime) -> Dict[str, Any]:
        return {
            'name#timestamp': f'{raid_name}#{raid_datetime.to_timestamp()}',
            'guild_id#group_id': f'{guild_id}#{group_id}'
        }

    def _table_kwargs(self):
        return {
            'KeySchema': [
                {
                    'AttributeName': 'name#timestamp',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'guild_id#group_id',
                    'KeyType': 'RANGE'
                }
            ],
            'AttributeDefinitions': [
                {
                    'AttributeName': 'name#timestamp',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'guild_id#group_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'guild_id',
                    'AttributeType': 'N'
                }
            ],
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 4,
                'WriteCapacityUnits': 4
            },
            'GlobalSecondaryIndexes': [
                {
                    'IndexName': RaidEventsTable.INDEX_NAME,
                    'KeySchema': [
                        {
                            'AttributeName': 'guild_id',
                            'KeyType': 'HASH'
                        },
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL',
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 1,
                        'WriteCapacityUnits': 1
                    }
                },
            ],
        }
