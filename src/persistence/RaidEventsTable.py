from typing import Optional, Dict, Any, List

from boto3.dynamodb.conditions import Key

from logic.RaidEvent import RaidEvent
from logic.Guild import Guild
from persistence.DynamoDBTable import DynamoDBTable
from datetime import datetime
from exceptions.InvalidInputException import InvalidInputException


class RaidEventsTable(DynamoDBTable[RaidEvent]):
    TABLE_NAME = 'raid_events'
    INDEX_NAME = 'guild_group_index'

    def __init__(self, ddb):
        super().__init__(ddb, RaidEventsTable.TABLE_NAME)

    def validate_raid_event(self, raid_event: RaidEvent):
        if None in [raid_event.name, raid_event.get_datetime(), raid_event.guild_id, raid_event.team_id]:
            return InvalidInputException(f"Raid {raid_event} has empty fields.")
        if raid_event.get_datetime() < datetime.now():
            raise InvalidInputException(f"Raid {raid_event} must be in future.")
        if self.get_raid_event(raid_event.guild_id, raid_event.team_id, raid_event.name, raid_event.datetime):
            raise InvalidInputException(f"Raid {raid_event} already exists.")

    def get_raid_event(self, guild_id: int, group_id: int, raid_name: str, raid_datetime: datetime) -> Optional[RaidEvent]:
        return super(RaidEventsTable, self).get_item(guild_id=guild_id, group_id=group_id,
                                                     raid_name=raid_name, raid_datetime=raid_datetime)

    def list_raid_events_for_guild(self, guild: Guild, since: float = 0) -> List[RaidEvent]:
        raid_events = []
        for raid_group in guild.raid_groups:
            raids_for_team = self.list_raid_events(guild.id, raid_group.id, since=since)
            raid_events.extend(raids_for_team)
        return raid_events

    def list_raid_events(self, guild_id: int, group_id: Optional[int], since: float = 0) -> List[RaidEvent]:
        key_condition = Key('guild_id#group_id').eq(f'{guild_id}#{group_id}') & Key('timestamp').gte(int(since))
        items = self.table.query(IndexName=RaidEventsTable.INDEX_NAME,
                                 KeyConditionExpression=key_condition)['Items']
        return [self._to_object(obj) for obj in items]

    def create_raid_event(self, raid_event: RaidEvent) -> None:
        self.validate_raid_event(raid_event)
        return super(RaidEventsTable, self).put_item(raid_event)

    def update_raid_event(self, raid_event: RaidEvent) -> None:
        return super(RaidEventsTable, self).put_item(raid_event)

    def remove_raid_event(self, raid_event: RaidEvent) -> bool:
        return super(RaidEventsTable, self).delete_item(guild_id=raid_event.guild_id, group_id=raid_event.team_id,
                                                        raid_name=raid_event.name, raid_datetime=raid_event.datetime)

    def _to_object(self, item: Dict[str, Any]) -> RaidEvent:
        item['name'], item['timestamp'] = tuple(item['name#timestamp'].split('#'))
        item['guild_id'], item['group_id'] = tuple(item['guild_id#group_id'].split('#'))
        return RaidEvent.from_dict(item)

    def _to_item(self, raid_event: RaidEvent) -> Dict[str, Any]:
        item = raid_event.to_dict()
        item['name#timestamp'] = item['name'] + '#' + str(item['timestamp'])
        item['guild_id#group_id'] = item['guild_id'] + '#' + item['group_id']
        return item

    def _to_key(self, guild_id: int, group_id: int, raid_name: str, raid_datetime: datetime) -> Dict[str, Any]:
        return {
            'name#timestamp': f'{raid_name}#{int(raid_datetime.timestamp())}',
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
                    'AttributeName': 'timestamp',
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
                            'AttributeName': 'guild_id#group_id',
                            'KeyType': 'HASH'
                        },
                        {
                            'AttributeName': 'timestamp',
                            'KeyType': 'RANGE'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL',
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 2,
                        'WriteCapacityUnits': 2
                    }
                },
            ],
        }
