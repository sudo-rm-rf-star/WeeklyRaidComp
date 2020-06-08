from logic.Guild import Guild
from typing import Dict, Any
from persistence.DynamoDBTable import DynamoDBTable


class GuildsTable(DynamoDBTable[Guild]):
    TABLE_NAME = 'guilds'

    def __init__(self, ddb):
        super().__init__(ddb, GuildsTable.TABLE_NAME)

    def get_guild(self, guild_id: int) -> Guild:
        return super(GuildsTable, self).get_item(guild_id=guild_id)

    def put_guild(self, guild: Guild) -> None:
        return super(GuildsTable, self).put_item(guild)

    def _to_object(self, item: Dict[str, Any]) -> Guild:
        return Guild.from_dict(item)

    def _to_item(self, raid_event: Guild) -> Dict[str, Any]:
        return raid_event.to_dict()

    def _to_key(self, guild_id: int):
        return {'guild_id': guild_id}

    def _table_kwargs(self):
        return {
            'KeySchema': [
                {
                    'AttributeName': 'guild_id',
                    'KeyType': 'HASH'
                },
            ],
            'AttributeDefinitions': [
                {
                    'AttributeName': 'guild_id',
                    'AttributeType': 'N'
                }
            ],
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 2,
                'WriteCapacityUnits': 2
            }
        }
