from .RaidEventHandler import RaidEventHandler
from .RaidEventUpdated import RaidEventUpdated


class RaidEventUpdatedHandler(RaidEventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def process(self, event: RaidEventUpdated):
        raid_event = self.get_raid(guild_id=event.guild_id, team_name=event.team_name, raid_name=event.raid_name,
                                   raid_datetime=event.raid_datetime)

        discord_guild = await self.get_discord_guild(event.guild_id, event.team_name)
        await discord_guild.sync_raid_message(raid_event)
