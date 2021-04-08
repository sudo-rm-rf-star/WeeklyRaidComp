import discord
from discord.ext.commands import Context
from exceptions.OngoingCommandException import OngoingCommandException

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
        message = await self.channel.send(content=content)
        await message.delete(delay=30)

    async def reply_to_author(self, content: str):
        await self.author.send(content=content)

    def __enter__(self):
        if (self.channel.id, self.author.id) in self.bot.interactions:
            raise OngoingCommandException()
        self.bot.interactions.add((self.channel.id, self.author.id))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.bot.interactions.remove((self.channel.id, self.author.id))
