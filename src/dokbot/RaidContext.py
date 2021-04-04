import discord
from dokbot.DokBot import DokBot
from dokbot.RaidTeamContext import RaidTeamContext
from persistence.RaidEventsResource import RaidEventsResource
from datetime import datetime
from logic.RaidEvent import RaidEvent


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

    @staticmethod
    def from_raid_team_context(ctx: RaidTeamContext, raid_event: RaidEvent):
        return RaidContext(bot=ctx.bot, guild=ctx.guild, author=ctx.author, channel=ctx.channel,
                           team_name=ctx.team_name, raid_name=raid_event.name, raid_datetime=raid_event.datetime)

    def __getattr__(self, item):
        if item == 'raid_event':
            self.raid_event = RaidEventsResource(self).get_raid(raid_name=self.raid_name,
                                                                raid_datetime=self.raid_datetime,
                                                                guild_id=self.guild_id, team_name=self.team_name)
            return self.raid_event
        return super(RaidContext, self).__getattr__(item)
