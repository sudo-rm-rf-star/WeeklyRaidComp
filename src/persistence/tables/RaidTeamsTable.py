from boto3.dynamodb.conditions import Key

from logic.RaidTeam import RaidTeam
from typing import Dict, Any, List
from persistence.tables.DynamoDBTable import DynamoDBTable


class RaidTeamsTable(DynamoDBTable[RaidTeam]):
    TABLE_NAME = 'raid_teams'

    def __init__(self, ddb):
        super().__init__(ddb, RaidTeamsTable.TABLE_NAME)

    def get_raidteam(self, team_name: str, guild_id: int) -> RaidTeam:
        return super(RaidTeamsTable, self).get_item(team_name=team_name, guild_id=guild_id)

    def create_raidteam(self, raid_team: RaidTeam) -> None:
        return super(RaidTeamsTable, self).put_item(raid_team)

    def update_raidteam(self, raid_team: RaidTeam) -> None:
        return super(RaidTeamsTable, self).put_item(raid_team)

    def list_raidteams(self, guild_id: int) -> List[RaidTeam]:
        return self.query(KeyConditionExpression=Key('guild_id').eq(str(guild_id)))

    def _to_object(self, item: Dict[str, Any]) -> RaidTeam:
        return RaidTeam.from_dict(item)

    def _to_item(self, raid_team: RaidTeam) -> Dict[str, Any]:
        return raid_team.to_dict()

    def _to_key(self, team_name: str, guild_id: int):
        return {'guild_id': str(guild_id), 'team_name': str(team_name)}

    def _table_kwargs(self):
        return {
            'KeySchema': [
                {
                    'AttributeName': 'guild_id',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'team_name',
                    'KeyType': 'RANGE'
                }
            ],
            'AttributeDefinitions': [
                {
                    'AttributeName': 'guild_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'team_name',
                    'AttributeType': 'S'
                }
            ],
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 2,
                'WriteCapacityUnits': 2
            }
        }
