import discord
from discord.ext.commands import Bot
from logic.Character import Character
from logic.enums.SignupStatus import SignupStatus

from dokbot.utils.DiscordUtils import get_emoji


class DokBot(Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.messages = {}
        self.channels = {}
        self.interactions = set()
        self.check(guild_only)

    async def emoji(self, emoji_name: str) -> discord.Emoji:
        return await get_emoji(self, emoji_name)

    async def message(self, channel_id: int, message_id: int) -> discord.Message:
        channel = await self.fetch_channel(channel_id)
        if message_id not in self.messages:
            self.messages[message_id] = await channel.fetch_message(message_id)
        return self.messages[message_id]

    async def fetch_channel(self, channel_id):
        if channel_id not in self.channels:
            self.channels[channel_id] = await super(DokBot, self).fetch_channel(channel_id)
        return self.channels[channel_id]

    async def display_character(self, character: Character, show_signup_indicator: bool = True) -> str:
        signup_choice = character.get_signup_status()
        visible_signup_statuses = [SignupStatus.Tentative, SignupStatus.Bench, SignupStatus.Late, SignupStatus.Decline]
        signup_indicator = await self.emoji(signup_choice.name) if signup_choice in visible_signup_statuses and show_signup_indicator else ''
        return f'{await self.emoji(character.klass.get_icon(character.spec))} {character.name} {signup_indicator}'


async def guild_only(ctx):
    if ctx.guild is None:
        await ctx.reply("I'm not the chatty type, sorry...")
        return False
    return True
