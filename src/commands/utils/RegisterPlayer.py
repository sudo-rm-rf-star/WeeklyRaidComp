from src.logic.enums.Class import Class
from src.logic.enums.Role import Role
from src.logic.enums.Race import Race
from src.logic.Player import Player
from src.logic.Players import Players
from src.client.GuildClient import GuildClient
from src.commands.utils.PlayerInteraction import interact, InteractionMessage, EnumResponseInteractionMessage
import src.client.Logger as Log
import discord

TRIES = 3


async def register(client: GuildClient, user: discord.Member, retry: bool = False) -> str:
    player = Players().get_by_id(user.id)
    if player is not None and not retry:
        message = f'You have already signed up: {player}'
        Log.warn(message)
        return message

    player_name = await interact(user, GetNameMesage(client))
    role = await interact(user, GetRoleMessage(client))
    klass = await interact(user, GetClassMessage(client))
    race = await interact(user, GetRaceMessage(client))
    player = Player(user.id, player_name, role=role, klass=klass, race=race)
    Players().add(player)
    Players().store()
    return f'You have successfully signed up: {player}'


class GetNameMesage(InteractionMessage):
    def __init__(self, client: GuildClient, *args, **kwargs):
        content = "Please respond with your character name"
        super(GetNameMesage, self).__init__(client, content, *args, **kwargs)

    async def get_response(self) -> str:
        return (await super(GetNameMesage, self).get_response()).capitalize()


class GetRoleMessage(EnumResponseInteractionMessage):
    def __init__(self, client: GuildClient, *args, **kwargs):
        content = "Please respond with the role of your character"
        super().__init__(client, content, Role, *args, **kwargs)


class GetClassMessage(EnumResponseInteractionMessage):
    def __init__(self, client: GuildClient, *args, **kwargs):
        content = "Please respond with the class of your character"
        super().__init__(client, content, Class, *args, **kwargs)


class GetRaceMessage(EnumResponseInteractionMessage):
    def __init__(self, client: GuildClient, *args, **kwargs):
        content = "Please respond with the race of your character"
        super().__init__(client, content, Race, *args, **kwargs)
