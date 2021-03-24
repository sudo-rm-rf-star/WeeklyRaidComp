import discord
from dokbot.DokBot import DokBot
from dokbot.DokBotContext import DokBotContext
from dokbot.DiscordUtils import get_channel
from persistence.RaidTeamsResource import RaidTeamsResource


class RaidTeamContext(DokBotContext):
    def __init__(self,
                 bot: DokBot,
                 guild: discord.Guild,
                 author: discord.User,
                 channel: discord.TextChannel,
                 team_name: str):
        super().__init__(bot=bot, guild=guild, author=author, channel=channel)
        self.team_name = team_name

    def __getattr__(self, item):
        if item == 'raid_team':
            self.raid_team = RaidTeamsResource().get_raidteam(guild_id=self.guild_id, team_name=self.team_name)
            return self.raid_team

    async def get_events_channel(self) -> discord.TextChannel:
        return await get_channel(guild=self.guild, channel_name=self.raid_team.events_channel)

