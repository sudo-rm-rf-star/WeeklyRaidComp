from client.DiscordClient import DiscordClient
from utils.EmojiNames import SIGNUP_STATUS_EMOJI
from logic.enums.SignupStatus import SignupStatus
from logic.RaidEvent import RaidEvent
from client.entities.DiscordMessage import DiscordMessage
from exceptions.InternalBotException import InternalBotException
from client.entities.GuildMember import GuildMember
import discord
import asyncio


class RaidNotification(DiscordMessage):
    def __init__(self, client: DiscordClient, raid_event: RaidEvent):
        self.client = client
        self.raid_event = raid_event
        content = f"You have been invited for {raid_event.get_name()} on {raid_event.datetime}. Please sign by clicking one of the reaction boxes."
        super(RaidNotification, self).__init__(content=content)

    async def send_to(self, recipient: GuildMember) -> discord.Message:
        msgs = await super(RaidNotification, self).send_to(recipient)
        if len(msgs) > 1:
            raise InternalBotException("Unhandled case")
        message = msgs[0]
        for emoji in [emoji_name for status, emoji_name in SIGNUP_STATUS_EMOJI.items() if status != SignupStatus.UNDECIDED]:
            asyncio.create_task(message.add_reaction(emoji=self.client.get_emoji(emoji)))
        return message
