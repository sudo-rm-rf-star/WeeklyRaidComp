from .RaidEventHandler import RaidEventHandler
from .RaidEventRemoved import RaidEventRemoved
from datetime import datetime


class RaidEventRemovedHandler(RaidEventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def process(self, event: RaidEventRemoved):
        raid_event = self.get_raid(guild_id=event.guild_id, team_name=event.team_name, raid_name=event.raid_name,
                                   raid_datetime=event.raid_datetime)

        discord_guild = await self.get_discord_guild(event.guild_id, event.team_name)

        for message_ref in raid_event.message_refs:
            message = await discord_guild.get_message(message_ref)
            if message:
                await message.delete()

        if raid_event.get_datetime() > datetime.now():
            await discord_guild.send_message_to_raiders(f'{raid_event} has been cancelled.')

        self.raids_resource.delete_raid(raid_event)
