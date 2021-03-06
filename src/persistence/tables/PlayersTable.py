from boto3.dynamodb.conditions import Key
from logic.Player import Player
from typing import Dict, Any
from persistence.tables.DynamoDBTable import DynamoDBTable
from typing import List, Optional
from logic.enums.Role import Role
from logic.enums.Class import Class
from logic.enums.Race import Race
from logic.Character import Character
from exceptions.InternalBotException import InternalBotException
from logic.Guild import Guild


class PlayersTable(DynamoDBTable[Player]):
    TABLE_NAME = 'players'
    INDEX_NAME = 'realm-region-index'

    def __init__(self, ddb):
        super().__init__(ddb, PlayersTable.TABLE_NAME)

    def get_player_by_name(self, player_name: str, guild: Guild) -> Optional[Player]:
        return _synthesize_player(self.table.query(IndexName=PlayersTable.INDEX_NAME,
                                                   KeyConditionExpression=index_expression(guild) & Key('name').eq(
                                                       player_name)))

    def get_player_by_id(self, discord_id: int) -> Optional[Player]:
        return _synthesize_player(self.table.query(KeyConditionExpression=Key('discord_id').eq(str(discord_id))))

    def list_players(self, guild: Guild) -> List[Player]:
        return [player for player in _synthesize_players(
            self.table.query(IndexName=PlayersTable.INDEX_NAME, KeyConditionExpression=index_expression(guild))) if
                guild.id in player.guild_ids]

    def put_player(self, player: Player) -> None:
        # TODO: optimization possible here, we don't always need to update all of the characters
        for character in player.characters:
            self.table.put_item(Item={
                'discord_id': str(player.discord_id),
                'realm#region': f'{player.realm}#{player.region}',
                'created_at': str(player.created_at),
                'selected_char': player.selected_char,
                'selected_raidgroup_id': str(player.selected_raidgroup_id),
                'name': character.name,
                'class': character.klass.name,
                'role': character.role.name,
                'race': character.race.name,
                'guild_ids': list(player.guild_ids),
                'selected_guild_id': player.selected_guild_id,
                'autoinvited': player.autoinvited
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
        selected_char = item.get('selected_char', None)
        selected_raidgroup_id = int(item['selected_raidgroup_id']) if item.get('selected_raidgroup_id',
                                                                               'None') != 'None' else None  # This isn't great
        char_name = item['name']
        klass = Class[item['class']]
        role = Role[item['role']]
        race = Race[item['race']]
        realm, region = tuple(item['realm#region'].split('#'))
        guild_ids = set(item.get('guild_ids', set()))
        selected_guild_id = item.get('selected_guild_id', item.get('last_guild_id', None))
        autoinvited = item.get('autoinvited', False)
        if discord_id not in players:
            players[discord_id] = Player(discord_id=discord_id, realm=realm, region=region, selected_char=selected_char,
                                         characters=[], created_at=created_at,
                                         selected_raidgroup_id=selected_raidgroup_id, guild_ids=guild_ids,
                                         selected_guild_id=selected_guild_id, autoinvited=autoinvited)
        player = players[discord_id]
        if realm != player.realm or region != player.region or selected_char != player.selected_char or \
                selected_raidgroup_id != player.selected_raidgroup_id or created_at != player.created_at or \
                guild_ids != player.guild_ids:
            print(guild_ids, player.guild_ids)
            raise InternalBotException("Player rows are not consistent.")
        player.characters.append(
            Character(char_name=char_name, discord_id=discord_id, klass=klass, role=role, race=race,
                      created_at=created_at))
    return list(players.values())


def _synthesize_player(items: Dict[str, Any]) -> Optional[Player]:
    players = _synthesize_players(items)
    if len(players) == 0:
        return None
    if len(players) != 1:
        raise InternalBotException("Invalid player count")
    return players[0]


def index_expression(guild: Guild):
    return Key('realm#region').eq(f'{guild.realm}#{guild.region}')
