from boto3.dynamodb.conditions import Key
from logic.Player import Player
from typing import Dict, Any
from persistence.DynamoDBTable import DynamoDBTable
from typing import List
from logic.enums.Role import Role
from logic.enums.Class import Class
from logic.enums.Race import Race
from logic.Character import Character
from exceptions.InternalBotException import InternalBotException


class PlayersTable(DynamoDBTable[Player]):
    TABLE_NAME = 'players'
    INDEX_NAME = 'guild_id_index'

    def __init__(self, ddb):
        super().__init__(ddb, PlayersTable.TABLE_NAME)

    def get_player_by_name(self, player_name: str, guild_id: int) -> Player:
        return _synthesize_player(
            self.table.query(IndexName=PlayersTable.INDEX_NAME, KeyConditionExpression=Key('guild_id').eq(guild_id) & Key('name').eq(player_name)))

    def get_player_by_id(self, discord_id: int) -> Player:
        return _synthesize_player(self.table.query(KeyConditionExpression=Key('discord_id').eq(discord_id)))

    def list_players(self, guild_id: int) -> List[Player]:
        return _synthesize_players(self.table.query(IndexName=PlayersTable.INDEX_NAME, KeyConditionExpression=Key('guild_id').eq(guild_id)))

    def put_player(self, player: Player) -> None:
        # TODO: optimalization possible here, we don't always need to update all of the characters
        for character in player.characters:
            self.table.put_item(Item={
                'discord_id': player.discord_id,
                'guild_id': player.guild_id,
                'present_dates': player.present_dates,
                'standby_dates': player.standby_dates,
                'selected_char': player.selected_char,
                'selected_raidgroup_id': player.selected_raidgroup_id,
                'name': character.name,
                'class': character.klass.name,
                'role': character.role.name,
                'race': character.race.name,
            })

    def _to_object(self, item: Dict[str, Any]) -> Player:
        raise InternalBotException("Should not be called")

    def _to_item(self, player: Player) -> Dict[str, Any]:
        raise InternalBotException("Should not be called")

    def _to_key(self, name: str):
        return {
            'name': name
        }

    def _table_kwargs(self):
        return {
            'KeySchema': [
                {
                    'AttributeName': 'discord_id',
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
                    'AttributeName': 'discord_id',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'guild_id',
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
                            'AttributeName': 'guild_id',
                            'KeyType': 'HASH'
                        },
                        {
                            'AttributeName': 'name',
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
                }
            ],

        }


def _synthesize_players(items: Dict[str, Any]) -> List[Player]:
    players = {}
    for item in items['Items']:
        char_name = item['name']
        klass = Class[item['class']]
        role = Role[item['role']]
        race = Race[item['race']]
        discord_id = item['discord_id']
        guild_id = item['guild_id']
        selected_char = item.get('selected_char', None)
        selected_raidgroup_id = item.get('selected_raidgroup_id', None)
        standby_dates = item.get('standby_dates', None)
        present_dates = item.get('present_dates', None)
        if discord_id not in players:
            players[discord_id] = Player(discord_id=discord_id, guild_id=guild_id, selected_char=selected_char, characters=[],
                                         present_dates=present_dates,
                                         standby_dates=standby_dates, selected_raidgroup_id=selected_raidgroup_id)
        player = players[discord_id]
        if guild_id != player.guild_id or selected_char != player.selected_char or selected_raidgroup_id != player.selected_raidgroup_id or \
                present_dates != player.present_dates or standby_dates != player.standby_dates:
            raise InternalBotException("Player rows are not consistent.")
        player.characters.append(Character(char_name=char_name, discord_id=discord_id, guild_id=guild_id, klass=klass, role=role, race=race,
                                           standby_count=player.get_standby_counts()))
    return list(players.values())


def _synthesize_player(items: Dict[str, Any]) -> Player:
    players = _synthesize_players(items)
    if len(players) != 1:
        raise InternalBotException("Invalid player count")
    return players[0]
