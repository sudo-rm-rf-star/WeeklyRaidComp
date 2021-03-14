from typing import Optional, Dict, Any, List, Union

from boto3.dynamodb.conditions import Key

from logic.RaidEvent import RaidEvent
from persistence.tables.DynamoDBTable import DynamoDBTable
from datetime import datetime
from exceptions.InvalidInputException import InvalidInputException


class RaidEventsTable(DynamoDBTable[RaidEvent]):
    TABLE_NAME = 'raid_events'
    INDEX_NAME = 'team-timestamp_index'

    def __init__(self, ddb):
        super().__init__(ddb, RaidEventsTable.TABLE_NAME)

    def validate_raid_event(self, raid_event: RaidEvent):
        if None in [raid_event.name, raid_event.get_datetime(), raid_event.team_name]:
            return InvalidInputException(f"Raid {raid_event} has empty fields.")
        if raid_event.get_datetime() < datetime.now():
            raise InvalidInputException(f"Raid {raid_event} must be in future.")
        if self.get_raid_event(raid_event.guild_id, raid_event.team_name, raid_event.name, raid_event.datetime):
            raise InvalidInputException(f"Raid {raid_event} already exists.")

    def get_raid_event(self, guild_id: int, team_name: str, raid_name: str, raid_datetime: datetime) -> Optional[RaidEvent]:
        return super(RaidEventsTable, self).get_item(guild_id=guild_id, team_name=team_name, raid_name=raid_name,
                                                     raid_datetime=raid_datetime)

    def list_raid_events(self, guild_id: int, raid_team_name: str,
                         since: Optional[Union[float, datetime]] = 0,
                         until: Optional[Union[float, datetime]] = None) -> List[RaidEvent]:
        if until and isinstance(until, datetime):
            until = until.timestamp()
        if since and isinstance(since, datetime):
            since = since.timestamp()

        key_condition = Key('guild_id#team_name').eq(f'{guild_id}#{raid_team_name}')
        if until:
            key_condition &= Key('timestamp').between(int(since), int(until))
        else:
            key_condition &= Key('timestamp').gte(int(since))

        items = self.table.query(IndexName=RaidEventsTable.INDEX_NAME,
                                 KeyConditionExpression=key_condition)['Items']
        return [self._to_object(obj) for obj in items]

    def create_raid_event(self, raid_event: RaidEvent) -> None:
        self.validate_raid_event(raid_event)
        return super(RaidEventsTable, self).put_item(raid_event)

    def update_raid_event(self, raid_event: RaidEvent) -> None:
        return super(RaidEventsTable, self).put_item(raid_event)

    def remove_raid_event(self, raid_event: RaidEvent) -> bool:
        return super(RaidEventsTable, self).delete_item(guild_id=raid_event.guild_id, team_name=raid_event.team_name,
                                                        raid_name=raid_event.name, raid_datetime=raid_event.datetime)

    def _to_object(self, item: Dict[str, Any]) -> RaidEvent:
        item['name'], item['guild_id'], item['team_name'] = tuple(item['name#guild_id#team_name'].split('#'))
        return RaidEvent.from_dict(item)

    def _to_item(self, raid_event: RaidEvent) -> Dict[str, Any]:
        item = raid_event.to_dict()
        item['name#guild_id#team_name'] = f'{raid_event.name}#{raid_event.guild_id}#{raid_event.team_name}'
        return item

    def _to_key(self, guild_id: int, team_name: str, raid_name: str, raid_datetime: datetime) -> Dict[str, Any]:
        return {
            'name#guild_id#team_name': f'{raid_name}#{guild_id}#{team_name}',
            'timestamp': int(raid_datetime.timestamp())
        }

    def _table_kwargs(self):
        return {
            'KeySchema': [
                {
                    'AttributeName': 'name#guild_id#team_name',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'timestamp',
                    'KeyType': 'RANGE'
                }
            ],
            'AttributeDefinitions': [
                {
                    'AttributeName': 'name#guild_id#team_name',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'timestamp',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'guild_id#team_name',
                    'AttributeType': 'S'
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
                            'AttributeName': 'guild_id#team_name',
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
