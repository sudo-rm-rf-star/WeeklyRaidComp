from discord.ext.commands import Bot, CheckFailure, check
import discord
from dokbot.DiscordUtils import get_emoji


class DokBot(Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.check(guild_only)

    async def emoji(self, emoji_name: str) -> discord.Emoji:
        return await get_emoji(self, emoji_name)

    async def message(self, channel_id: int, message_id: int) -> discord.Message:
        channel = await self.fetch_channel(channel_id)
        return await channel.fetch_message(message_id)


class NoPrivateMessages(CheckFailure):
    pass


async def guild_only(ctx):
    if ctx.guild is None:
        await ctx.reply('Hey no DMs!')
        return False
    return True
