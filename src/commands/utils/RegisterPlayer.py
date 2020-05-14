from logic.enums.Class import Class
from logic.enums.Role import Role
from logic.enums.Race import Race
from logic.Player import Player
from client.DiscordClient import DiscordClient
from commands.utils.PlayerInteraction import interact, InteractionMessage, EnumResponseInteractionMessage
from client.entities.GuildMember import GuildMember
from client.PlayersResource import PlayersResource
import asyncio

TRIES = 3


async def register(client: DiscordClient, players_resource: PlayersResource, member: GuildMember, retry: bool = False) -> Player:
    player = players_resource.get_player_by_id(member.id)
    if player is not None and not retry:
        member.send(f'You have already signed up: {player}')
        return player

    player_name = await interact(member, GetNameMesage(client))
    role = await interact(member, GetRoleMessage(client))
    klass = await interact(member, GetClassMessage(client))
    race = await interact(member, GetRaceMessage(client))
    player = Player(discord_id=member.id, char_name=player_name, role=role, klass=klass, race=race)
    players_resource.update_player(player)
    asyncio.create_task(member.send(content=f'You have successfully registered: {player}'))
    return player


class GetNameMesage(InteractionMessage):
    def __init__(self, client: DiscordClient, *args, **kwargs):
        content = "Please respond with your character name"
        super(GetNameMesage, self).__init__(client, content, *args, **kwargs)

    async def get_response(self) -> str:
        return (await super(GetNameMesage, self).get_response()).capitalize()


class GetRoleMessage(EnumResponseInteractionMessage[Role]):
    def __init__(self, client: DiscordClient, *args, **kwargs):
        content = "Please respond with the role of your character"
        super().__init__(client, content, Role, *args, **kwargs)


class GetClassMessage(EnumResponseInteractionMessage[Class]):
    def __init__(self, client: DiscordClient, *args, **kwargs):
        content = "Please respond with the class of your character"
        super().__init__(client, content, Class, *args, **kwargs)


class GetRaceMessage(EnumResponseInteractionMessage[Race]):
    def __init__(self, client: DiscordClient, *args, **kwargs):
        content = "Please respond with the race of your character"
        super().__init__(client, content, Race, *args, **kwargs)
