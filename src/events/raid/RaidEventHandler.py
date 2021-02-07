from persistence.RaidEventsResource import RaidEventsResource
from events.EventHandler import EventHandler
from exceptions.InternalBotException import InternalBotException
from datetime import datetime


class RaidEventHandler(EventHandler):
    def __init__(self, *args, **kwargs):
        self.raids_resource = RaidEventsResource()
        super(RaidEventHandler, self).__init__(*args, **kwargs)

    def get_raid(self, guild_id: int, team_name: str, raid_name: str, raid_datetime: datetime):
        raid_event = self.raids_resource.get_raid(guild_id=guild_id, team_name=team_name, raid_name=raid_name,
                                                  raid_datetime=raid_datetime)
        if raid_event is None:
            raise InternalBotException(
                f'Could not find raid event {guild_id}/{team_name}/{raid_name},{raid_datetime}')
        return raid_event
