from utils.EmojiNames import SIGNUP_STATUS_EMOJI
from logic.enums.SignupStatus import SignupStatus
from logic.RaidEvent import RaidEvent
from client.entities.DiscordMessage import DiscordMessage
from client.entities.GuildMember import GuildMember
import discord
from utils.DiscordUtils import get_emoji
import utils.Logger as Log
from typing import Optional


class RaidNotification(DiscordMessage):
    def __init__(self, client: discord.Client, guild: discord.Guild, raid_event: RaidEvent):
        self.client = client
        self.raid_event = raid_event
        content = f"You have been invited for {raid_event}. Please sign by clicking one of the reaction boxes."
        super(RaidNotification, self).__init__(client, guild, content=content)

    async def send_to(self, recipient: GuildMember) -> Optional[discord.Message]:
        msgs = await super(RaidNotification, self).send_to(recipient)
        if len(msgs) == 1:
            message = msgs[0]
            for emoji in [emoji_name for status, emoji_name in SIGNUP_STATUS_EMOJI.items() if status != SignupStatus.UNDECIDED]:
                await message.add_reaction(emoji=get_emoji(self.discord_guild, emoji))
            return message
        else:
            Log.error(f'Could not send message to {recipient}')
            return None
