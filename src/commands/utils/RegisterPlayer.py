from src.logic.enums.Class import Class
from src.logic.enums.Role import Role
from src.logic.enums.Race import Race
from src.exceptions.InvalidArgumentException import InvalidArgumentException
from src.logic.Player import Player
from src.logic.Players import Players
from src.client.entities.DiscordMessage import DiscordMessage
from src.client.GuildClient import GuildClient
from typing import Generic, TypeVar, Union
import discord

TRIES = 3


async def register(client: GuildClient, user: discord.Member) -> str:
    player = Players().get_by_id(user.id)
    if player is not None:
        return f'You have already signed up: {player}'

    player_name = await _interaction(user, GetNameMesage(client))
    role = await _interaction(user, GetRoleMessage(client))
    klass = await _interaction(user, GetClassMessage(client))
    race = await _interaction(user, GetRaceMessage(client))
    player = Player(user.id, player_name, role=role, klass=klass, race=race)
    Players().add(player)
    return f'You have successfully signed up: {player}'


class InteractionMessage(DiscordMessage):
    def __init__(self, client: GuildClient, content: str, *args, **kwargs):
        self.client = client
        super(InteractionMessage, self).__init__(content, *args, **kwargs)
        # These variables will be filled once the message is sent
        self.channel_id = None
        self.recipient_id = None

    async def get_response(self) -> str:
        msg = await self.client.wait_for('message', check=lambda response: _check_if_response(self, response))
        return msg.content

    async def send_to(self, recipient: Union[discord.Member, discord.TextChannel]) -> discord.Message:
        msg = await super(InteractionMessage, self).send_to(recipient)
        self.channel_id = msg.channel.id
        self.recipient_id = recipient.id
        return msg


def _check_if_response(interaction_msg: InteractionMessage, msg: discord.Message):
    assert interaction_msg.channel_id and interaction_msg.recipient_id, "There's no message to get a response for"
    return interaction_msg.channel_id == msg.channel.id and interaction_msg.recipient_id == msg.author.id


class GetNameMesage(InteractionMessage):
    def __init__(self, client: GuildClient, *args, **kwargs):
        content = "Please respond with your character name"
        super(GetNameMesage, self).__init__(client, content, *args, **kwargs)

    async def get_response(self) -> str:
        return (await super(GetNameMesage, self).get_response()).capitalize()


T = TypeVar('T')


class EnumResponseInteractionMessage(InteractionMessage, Generic[T]):
    def __init__(self, client: GuildClient, content: str, enum: T, *args, **kwargs):
        self.options = [' '.join(map(lambda x: x.capitalize(), value.split('_'))) for value in enum.__members__.keys()]
        self.enum = enum
        content += f': {self.options}'
        super().__init__(client, content, *args, **kwargs)

    async def get_response(self) -> T:
        response = await super(EnumResponseInteractionMessage, self).get_response()
        option = response.replace(' ', '').upper()
        try:
            return self.enum[option]
        except KeyError:
            raise InvalidArgumentException(f'Please choose on of: {self.options}')


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


async def _interaction(member: discord.Member, message: InteractionMessage) -> str:
    await message.send_to(member)
    response = None
    trie = 0
    while not response:
        try:
            response = await message.get_response()
        except InvalidArgumentException as ex:
            if trie < TRIES:
                raise InvalidArgumentException("Exceeded retries, aborting signup.")
            await member.send(content=str(ex))
            trie += 1

    return response
