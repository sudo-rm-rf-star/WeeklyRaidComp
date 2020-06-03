from boto3.dynamodb.conditions import Key
from logic.Player import Player
from typing import Dict, Any
from persistence.DynamoDBTable import DynamoDBTable
from typing import List


class PlayersTable(DynamoDBTable[Player]):
    TABLE_NAME = 'players'
    INDEX_NAME = 'discord_id_index'

    def __init__(self, ddb):
        super().__init__(ddb, PlayersTable.TABLE_NAME)

    def get_player(self, player_name: str) -> Player:
        return super(PlayersTable, self).get_item(name=player_name)

    def put_player(self, player: Player) -> None:
        return super(PlayersTable, self).put_item(player)

    def remove_player(self, player_name: str) -> bool:
        return super(PlayersTable, self).remove_item(name=player_name)

    def get_players_by_id(self, discord_id) -> List[Player]:
        players = self.table.query(IndexName=PlayersTable.INDEX_NAME, KeyConditionExpression=Key('discord_id').eq(discord_id))
        return [self._to_object(player) for player in players['Items']]

    def _to_object(self, item: Dict[str, Any]) -> Player:
        return Player.from_dict(item)

    def _to_item(self, player: Player) -> Dict[str, Any]:
        return player.to_dict()

    def _to_key(self, name: str):
        return {
            'name': name
        }

    def _table_kwargs(self):
        return {
            'KeySchema': [
                {
                    'AttributeName': 'name',
                    'KeyType': 'HASH'
                }
            ],
            'AttributeDefinitions': [
                {
                    'AttributeName': 'name',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'discord_id',
                    'AttributeType': 'N'
                }
            ],
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 3,
                'WriteCapacityUnits': 3
            },
            'GlobalSecondaryIndexes': [
                {
                    'IndexName': PlayersTable.INDEX_NAME,
                    'KeySchema': [
                        {
                            'AttributeName': 'discord_id',
                            'KeyType': 'HASH'
                        },
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL',
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 3,
                        'WriteCapacityUnits': 3
                    }
                },
            ],

        }
