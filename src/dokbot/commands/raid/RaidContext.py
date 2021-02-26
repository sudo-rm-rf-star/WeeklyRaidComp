import discord
from dokbot.DokBot import DokBot
from dokbot.DokBotContext import DokBotContext


class RaidContext(DokBotContext):
    def __init__(self,
                 bot: DokBot,
                 guild: discord.Guild,
                 author: discord.User,
                 channel: discord.TextChannel,
                 team_name: str):
        super().__init__(bot=bot, guild=guild, author=author, channel=channel)
        self.team_name = team_name
