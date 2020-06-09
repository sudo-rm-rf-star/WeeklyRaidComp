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

TRIES = 3


async def register(client: discord.Client, guild: discord.Guild, players_resource: PlayersResource, member: GuildMember,
                   allow_multiple_chars: bool = False) -> Player:
    player = players_resource.get_player_by_id(member.id)
    if len(player.characters) >= 1 and not allow_multiple_chars:
        member.send(f'You have already signed up: {player}')
        return player

    char_name = await interact(member, GetNameMesage(client, guild))
    role = await interact(member, GetRoleMessage(client, guild))
    klass = await interact(member, GetClassMessage(client, guild))
    race = await interact(member, GetRaceMessage(client, guild))
    if not player:
        player = Player(discord_id=member.id, guild_id=member.guild_id, characters=[], selected_char=char_name, created_at=datetime.now().timestamp())
    character = Character(discord_id=member.id, guild_id=guild.id, char_name=char_name, role=role, klass=klass, race=race,
                          standby_count=player.get_standby_counts())
    player.characters.append(character)
    players_resource.update_player(player)
    asyncio.create_task(member.send(content=f'You have successfully registered: {character}'))
    return player


class GetNameMesage(InteractionMessage):
    def __init__(self, client: discord.Client, guild: discord.Guild, *args, **kwargs):
        content = "Please respond with your character name"
        super(GetNameMesage, self).__init__(client, guild, content, *args, **kwargs)

    async def get_response(self) -> str:
        return (await super(GetNameMesage, self).get_response()).capitalize()


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
