from exceptions.InternalBotException import InternalBotException
from exceptions.InvalidInputException import InvalidInputException
from client.entities.DiscordMessage import DiscordMessage
from typing import Generic, TypeVar, Union, Any
import discord
from client.entities.GuildMember import GuildMember
from exceptions.CancelInteractionException import CancelInteractionException
from typing import Optional

TRIES = 3


class InteractionMessage(DiscordMessage):
    def __init__(self, client: discord.Client, guild: discord.Guild, content: str, *args, **kwargs):
        self.client = client
        super(InteractionMessage, self).__init__(client, guild, content, *args, **kwargs)
        # These variables will be filled once the message is sent
        self.channel_id = None
        self.recipient_id = None

    async def get_response(self) -> Optional[str]:
        msg = await self.client.wait_for('message', check=lambda response: _check_if_response(self, response))
        content = msg.content
        if content.strip() == 'skip':
            return None
        if content.strip() == '!done':
            raise CancelInteractionException()
        return content

    async def send_to(self, recipient: Union[GuildMember, discord.TextChannel]) -> discord.Message:
        msgs = await super(InteractionMessage, self).send_to(recipient)
        if len(msgs) > 1:
            raise InternalBotException("Unhandled case")
        msg = msgs[0]
        self.channel_id = msg.channel.id
        self.recipient_id = recipient.id
        return msg


def _check_if_response(interaction_msg: InteractionMessage, msg: discord.Message):
    assert interaction_msg.channel_id and interaction_msg.recipient_id, "There's no message to get a response for"
    return interaction_msg.channel_id == msg.channel.id and interaction_msg.recipient_id == msg.author.id


T = TypeVar('T')


class EnumResponseInteractionMessage(InteractionMessage, Generic[T]):
    def __init__(self, client: discord.Client, guild: discord.Guild, content: str, enum: T, *args, **kwargs):
        self.enum = enum
        self.options = '/'.join([' '.join(map(lambda x: x.capitalize(), value.split('_'))) for value in enum.__members__.keys()])
        content += f': {self.options}'
        super().__init__(client, guild, content, *args, **kwargs)

    async def get_response(self) -> Optional[T]:
        response = await super(EnumResponseInteractionMessage, self).get_response()
        if not response:
            return None
        option = response.replace(' ', '').upper()
        try:
            return self.enum[option]
        except KeyError:
            raise InvalidInputException(f'Please choose on of: {self.options}')


async def interact(member: GuildMember, message: InteractionMessage) -> Any:
    await message.send_to(member)
    response = None
    finished = False
    trie = 0
    while not finished:
        try:
            response = await message.get_response()
            finished = True
        except InvalidInputException as ex:
            if trie >= TRIES:
                raise InvalidInputException("Exceeded retries, aborting signup.")
            await member.send(content=str(ex))
            trie += 1

    return response

