from .RaidEventHandler import RaidEventHandler
from .RaidEventCreated import RaidEventCreated
from dokbot.entities.RaidMessage import RaidMessage
from dokbot.entities.RaidNotification import RaidNotification


class RaidEventCreatedHandler(RaidEventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def process(self, event: RaidEventCreated):
        ctx = await self.get_context(event)
        await RaidMessage.send_message(ctx=ctx)
        raid_event = self.get_raid(guild_id=event.guild_id, team_name=event.team_name, raid_name=event.raid_name,
                                   raid_datetime=event.raid_datetime)
        await RaidMessage.send_message(ctx)
        await RaidNotification.send_messages(ctx)
        self.raids_resource.update_raid(raid_event)
