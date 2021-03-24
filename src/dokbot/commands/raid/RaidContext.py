import discord
from dokbot.DokBot import DokBot
from dokbot.commands.raidteam.RaidTeamContext import RaidTeamContext
from persistence.RaidEventsResource import RaidEventsResource
from datetime import datetime


class RaidContext(RaidTeamContext):
    def __init__(self,
                 bot: DokBot,
                 guild: discord.Guild,
                 author: discord.User,
                 channel: discord.TextChannel,
                 team_name: str,
                 raid_name: str,
                 raid_datetime: datetime):
        self.raid_name = raid_name
        self.raid_datetime = raid_datetime
        super().__init__(bot=bot, guild=guild, author=author, channel=channel, team_name=team_name)

    def __getattr__(self, item):
        if item == 'raid_event':
            self.raid_event = RaidEventsResource().get_raid(raid_name=self.raid_name, raid_datetime=self.raid_datetime,
                                                            guild_id=self.guild_id, team_name=self.team_name)
            return self.raid_event
        return super(RaidContext, self).__getattr__(item)
