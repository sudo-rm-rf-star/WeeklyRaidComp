from logic.enums.Class import Class
from logic.Character import Character
from logic.enums.Role import Role
from logic.enums.Race import Race
from logic.Player import Player
from commands.utils.PlayerInteraction import interact, InteractionMessage, EnumResponseInteractionMessage
from client.entities.GuildMember import GuildMember
from client.PlayersResource import PlayersResource
import asyncio
import discord
from datetime import datetime
import re
from exceptions.InvalidArgumentException import InvalidArgumentException
from typing import Tuple, Optional
from logic.Guild import Guild

TRIES = 3


async def register(client: discord.Client, guild: Guild, players_resource: PlayersResource, member: GuildMember,
                   allow_multiple_chars: bool = False) -> Tuple[Player, Optional[Character]]:
    player = players_resource.get_player_by_id(member.id)
    if player and len(player.characters) >= 1 and not allow_multiple_chars:
        member.send(f'You have already signed up: {player}')
        return player, None

    char_name = await interact(member, GetNameMesage(client, guild))
    role = await interact(member, GetRoleMessage(client, guild))
    klass = await interact(member, GetClassMessage(client, guild))
    race = await interact(member, GetRaceMessage(client, guild))
    if player is None:
        player = Player(discord_id=member.id, realm=guild.realm, region=guild.region, characters=[],
                        selected_char=char_name, created_at=datetime.now().timestamp())
    character = Character(discord_id=member.id, char_name=char_name, role=role, klass=klass, race=race,
                          created_at=datetime.now().timestamp(), standby_dates={})
    player.characters.append(character)
    players_resource.update_player(player)
    asyncio.create_task(member.send(content=f'You have successfully registered: {character}'))
    return player, character


class GetNameMesage(InteractionMessage):
    def __init__(self, client: discord.Client, guild: discord.Guild, *args, **kwargs):
        content = "Please respond with your character name"
        super(GetNameMesage, self).__init__(client, guild, content, *args, **kwargs)

    async def get_response(self) -> str:
        name = (await super(GetNameMesage, self).get_response()).strip().capitalize()
        if re.search(r"\s", name):
            raise InvalidArgumentException(f'Please use your character name')
        return name


class GetRoleMessage(EnumResponseInteractionMessage[Role]):
    def __init__(self, client: discord.Client, guild: discord.Guild, *args, **kwargs):
        content = "Please respond with the role of your character"
        super().__init__(client, guild, content, Role, *args, **kwargs)


class GetClassMessage(EnumResponseInteractionMessage[Class]):
    def __init__(self, client: discord.Client, guild: discord.Guild, *args, **kwargs):
        content = "Please respond with the class of your character"
        super().__init__(client, guild, content, Class, *args, **kwargs)


class GetRaceMessage(EnumResponseInteractionMessage[Race]):
    def __init__(self, client: discord.Client, guild: discord.Guild, *args, **kwargs):
        content = "Please respond with the race of your character"
        super().__init__(client, guild, content, Race, *args, **kwargs)
