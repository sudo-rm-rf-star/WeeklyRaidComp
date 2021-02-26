from exceptions.InternalBotException import InternalBotException
from typing import List
from dokbot.entities.DiscordMessage import DiscordMessage
from typing import Union, Any
import discord
from dokbot.entities.discord.Member import discord.Member
from typing import Optional

TRIES = 3


class EmojiInteractionMessage(DiscordMessage):
    def __init__(self, client: discord.Client, guild: discord.Guild, content: str, reactions: List[str], *args, **kwargs):
        self.client = client
        super(EmojiInteractionMessage, self).__init__(client, guild, content=content, reactions=reactions, *args, **kwargs)
        # These variables will be filled once the message is sent
        self.channel_id = None
        self.recipient_id = None

    @classmethod
    async def interact(cls, member: discord.Member, client: discord.Client, guild: discord.Guild, *args, **kwargs) -> Any:
        msg = cls(client=client, guild=guild, member=member, *args, **kwargs)
        await msg.send_to(member)
        return await msg.get_response()

    async def get_response(self) -> Optional[str]:
        def check(reaction, user):
            return user.id == self.recipient_id and reaction.emoji.name in self.emojis
        (reaction, user) = await self.client.wait_for('reaction_add', check=check)
        return reaction.emoji.name

    async def send_to(self, recipient: Union[discord.Member, discord.TextChannel]) -> discord.Message:
        msgs = await super(EmojiInteractionMessage, self).send_to(recipient)
        if len(msgs) > 1:
            raise InternalBotException("Unhandled case")
        msg = msgs[0]
        self.channel_id = msg.channel.id
        self.recipient_id = recipient.id
        return msg
