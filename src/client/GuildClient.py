import discord
from src.common.Constants import GUILD, BOT_NAME
from typing import List, Any, Tuple, Optional
from datetime import datetime


class GuildClient:
    def __init__(self, client: discord.Client, guild: discord.Guild):
        self.client = client
        self.guild = guild

    async def get_guild(self) -> discord.Guild:
        return await discord.utils.get(self.client.fetch_guilds(), name=GUILD)

    def get_bot(self, bot_name: str = BOT_NAME) -> discord.User:
        return discord.utils.get(self.guild.members, name=bot_name)

    def get_channel(self, channel_name: str) -> discord.TextChannel:
        return discord.utils.get(self.guild.text_channels, name=channel_name)

    def get_channel_by_id(self, channel_id: int) -> discord.TextChannel:
        return discord.utils.get(self.guild.text_channels, id=channel_id)

    def get_emoji(self, emoji_name: str) -> discord.Emoji:
        return discord.utils.get(self.guild.emojis, name=emoji_name)

    def get_member(self, user_name: str) -> discord.Member:
        return self.guild.get_member_named(user_name)

    def get_member_by_id(self, user_id: int) -> discord.Member:
        return self.guild.get_member(user_id)

    def get_users(self) -> List[discord.Member]:
        return self.guild.members

    def get_role(self, role_name: str) -> discord.Role:
        return discord.utils.get(self.guild.roles, name=role_name)

    def get_members_for_role(self, role_name: str) -> List[discord.Member]:
        return self.get_role(role_name).members

    async def get_message(self, message_id_pair: Tuple[int, int], after: Optional[datetime] = None) -> discord.Message:
        message_id, recipient_id = message_id_pair  # This can be a user id or text channel id
        text_channel = self.get_channel_by_id(recipient_id)
        if not text_channel:
            text_channel = self.get_member_by_id(recipient_id).dm_channel
        return await text_channel.fetch_message(message_id)

    def wait_for(self, *args, **kwargs) -> Any:
        return self.client.wait_for(*args, **kwargs)

