from utils.EmojiNames import SIGNUP_STATUS_EMOJI
from logic.RaidEvent import RaidEvent
from client.entities.DiscordMessage import DiscordMessage
from client.entities.GuildMember import GuildMember
import discord
import utils.Logger as Log
from typing import Optional


class RaidNotification(DiscordMessage):
    def __init__(self, client: discord.Client, guild: discord.Guild, raid_event: RaidEvent):
        self.client = client
        self.raid_event = raid_event
        content = f"You have been invited for {raid_event}. Please sign by clicking one of the reaction boxes."
        super(RaidNotification, self).__init__(client, guild, content=content)

    async def send_to(self, recipient: GuildMember) -> Optional[discord.Message]:
        Log.info(f'Inviting {recipient} to {self.raid_event}')
        msgs = await super(RaidNotification, self).send_to(recipient)
        if len(msgs) == 1:
            message = msgs[0]
            for emoji in [emoji_name for status, emoji_name in SIGNUP_STATUS_EMOJI.items()]:
                try:
                    await message.add_reaction(emoji=self._get_emoji(emoji))
                except discord.NotFound:
                    Log.error(f'Could not find {emoji} when sending to {recipient}')
            return message
        else:
            Log.error(f'Could not send message to {recipient}')
            return None
