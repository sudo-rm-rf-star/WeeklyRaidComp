import discord
from discord.ext.commands import Context

from .DokBot import DokBot


class DokBotContext:
    def __init__(self, bot: DokBot, guild: discord.Guild, author: discord.User, channel: discord.TextChannel):
        self.bot = bot
        self.guild = guild
        self.author = author
        self.channel = channel
        self.guild_id = self.guild.id

    @staticmethod
    def from_context(ctx: Context):
        return DokBotContext(bot=ctx.bot, guild=ctx.guild, author=ctx.author, channel=ctx.channel)

    async def reply(self, content: str):
        await self.channel.send(content=content)

    async def reply_to_author(self, content: str):
        await self.author.send(content=content)
