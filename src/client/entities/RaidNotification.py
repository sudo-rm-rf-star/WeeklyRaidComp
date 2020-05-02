from src.client.GuildClient import GuildClient
from src.common.EmojiNames import SIGNUP_STATUS_EMOJI
from src.logic.enums.SignupStatus import SignupStatus
from src.logic.RaidEvent import RaidEvent
from src.client.entities.DiscordMessage import DiscordMessage
import discord
import asyncio


class RaidNotification(DiscordMessage):
    def __init__(self, client: GuildClient, raid_event: RaidEvent):
        self.client = client
        self.raid_event = raid_event
        content = f"You have been invited for {raid_event.name} on {raid_event.datetime}. Please sign by clicking one of the reaction boxes."
        super(RaidNotification, self).__init__(content=content)

    async def send_to(self, recipient: discord.Member) -> discord.Message:
        message = await super(RaidNotification, self).send_to(recipient)
        for emoji in [emoji_name for status, emoji_name in SIGNUP_STATUS_EMOJI.items() if status != SignupStatus.UNDECIDED]:
            asyncio.create_task(message.add_reaction(emoji=self.client.get_emoji(emoji)))
        return message
