import discord
from utils.Constants import GUILD, BOT_NAME
from typing import List, Any
from exceptions.InternalBotException import InternalBotException
from client.entities.GuildMember import GuildMember
from client.entities.DiscordMessageIdentifier import DiscordMessageIdentifier


class DiscordClient:
    def __init__(self, client: discord.Client):
        self.client = client
        self.guild = None

    async def on_ready(self):
        guilds = await self.client.fetch_guilds().flatten()
        guild = discord.utils.get(guilds, name=GUILD)
        self.guild = self.client.get_guild(guild.id)
        self.id = self.client.user.id

    def is_ready(self):
        return self.guild is not None

    async def get_guild(self) -> discord.Guild:
        return await discord.utils.get(self.client.fetch_guilds(), name=GUILD)

    def get_bot(self, bot_name: str = BOT_NAME) -> discord.User:
        return discord.utils.get(self.guild.members, name=bot_name)

    def get_channel(self, channel_name: str) -> discord.TextChannel:
        return discord.utils.get(self.guild.text_channels, name=channel_name)

    async def get_channel_by_id(self, channel_id: int) -> discord.TextChannel:
        return await self.client.fetch_channel(channel_id)

    def get_emoji(self, emoji_name: str) -> discord.Emoji:
        return discord.utils.get(self.guild.emojis, name=emoji_name)

    def get_member(self, user_name: str) -> GuildMember:
        return GuildMember(self.guild.get_member_named(user_name))

    def get_member_by_id(self, user_id: int) -> GuildMember:
        return GuildMember(self.guild.get_member(user_id))

    def get_users(self) -> List[GuildMember]:
        return [GuildMember(member) for member in self.guild.members]

    def get_role(self, role_name: str) -> discord.Role:
        return discord.utils.get(self.guild.roles, name=role_name)

    def get_members_for_role(self, role_name: str) -> List[GuildMember]:
        return [GuildMember(member) for member in self.get_role(role_name).members]

    async def get_message(self, message_id: DiscordMessageIdentifier) -> discord.Message:
        text_channel = await self.get_channel_by_id(message_id.channel_id)
        try:
            return await text_channel.fetch_message(message_id.message_id)
        except discord.NotFound:
            raise InternalBotException("Could not find message")

    def wait_for(self, *args, **kwargs) -> Any:
        return self.client.wait_for(*args, **kwargs)

