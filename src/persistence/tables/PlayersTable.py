from boto3.dynamodb.conditions import Key
from logic.Player import Player
from typing import Dict, Any
from persistence.tables.DynamoDBTable import DynamoDBTable
from typing import List, Optional
from logic.enums.Role import Role
from logic.enums.Class import Class
from logic.Character import Character
from exceptions.InternalBotException import InternalBotException
from logic.RaidTeam import RaidTeam


class PlayersTable(DynamoDBTable[Player]):
    TABLE_NAME = 'players'
    INDEX_NAME = 'realm-region-index'

    def __init__(self, ddb):
        super().__init__(ddb, PlayersTable.TABLE_NAME)

    def get_player_by_name(self, player_name: str, raid_team: RaidTeam) -> Optional[Player]:
        # key_condition_expression = index_expression(raid_team) & Key('name').eq(player_name)
        key_condition_expression = Key('name').eq(player_name)
        # query_result = self.table.query(IndexName=PlayersTable.INDEX_NAME,
        #                                 KeyConditionExpression=key_condition_expression)
        query_result = self.table.query(KeyConditionExpression=key_condition_expression)

        return _synthesize_player(query_result)

    def get_player_by_id(self, discord_id: int) -> Optional[Player]:
        return _synthesize_player(self.table.query(KeyConditionExpression=Key('discord_id').eq(str(discord_id))))

    def put_player(self, player: Player) -> None:
        for character in player.characters:
            self.table.put_item(Item={
                'discord_id': str(player.discord_id),
                'realm#region': f'{player.realm}#{player.region}',
                'created_at': str(player.created_at),
                'name': character.name,
                'class': character.klass.name,
                'role': character.role.name,
                'spec': character.spec,
                'selected_char': player.selected_char,
                'selected_guild_id': player.selected_guild_id,
                'selected_team_name': player.selected_team_name
            })

    def remove_character(self, character: Character):
        self.delete_item(name=character.name, discord_id=character.discord_id)

    def _to_object(self, item: Dict[str, Any]) -> Player:
        raise InternalBotException("Should not be called")

    def _to_item(self, player: Player) -> Dict[str, Any]:
        raise InternalBotException("Should not be called")

    def _to_key(self, name: str, discord_id: int):
        return {
            'discord_id': str(discord_id),
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
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'realm#region',
                    'AttributeType': 'S'
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
                            'AttributeName': 'realm#region',
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
        discord_id = int(item['discord_id'])
        created_at = float(item['created_at'])
        char_name = item['name']
        klass = Class[item['class']]
        role = Role[item['role']]
        spec = item.get('spec')
        realm, region = tuple(item['realm#region'].split('#'))
        # BUGFIXES UNTIL NEXT VERSION
        if not realm:
            realm = "Earthshaker"
        if not region:
            region = "EU"
        selected_char = item.get('selected_char')
        selected_team_name = item.get('selected_team_name')
        selected_guild_id = item.get('selected_guild_id')
        if discord_id not in players:
            players[discord_id] = Player(discord_id=discord_id, realm=realm, region=region, selected_char=selected_char,
                                         characters=[], created_at=created_at, selected_team_name=selected_team_name,
                                         selected_guild_id=selected_guild_id)
        player = players[discord_id]
        if realm != player.realm or region != player.region or selected_char != player.selected_char or \
                selected_team_name != player.selected_team_name or created_at != player.created_at:
            raise InternalBotException("Player rows are not consistent.")
        player.characters.append(
            Character(char_name=char_name, discord_id=discord_id, klass=klass, role=role, spec=spec,
                      created_at=created_at))
    return list(players.values())


def _synthesize_player(items: Dict[str, Any]) -> Optional[Player]:
    players = _synthesize_players(items)
    if len(players) == 0:
        return None
    if len(players) != 1:
        raise InternalBotException("Invalid player count")
    return players[0]


def index_expression(raid_team: RaidTeam):
    return Key('realm#region').eq(f'{raid_team.realm}#{raid_team.region}')
