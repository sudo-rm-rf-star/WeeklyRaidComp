from typing import Dict, Tuple

from events.EventQueue import EventQueue
from events.raid.RosterUpdated import RosterUpdated
from persistence.RaidEventsResource import RaidEventsResource


class RaidController:
    def __init__(self, *args, **kwargs):
        super(RaidController, self).__init__(*args, **kwargs)
        self.event_queue = EventQueue()
        self.raids_resource = RaidEventsResource()

    def get(self, token: str):
        raid = self.raids_resource.get_raid_by_token(token)
        return {'data': raid.to_dict() if raid else None}

    def publish_roster_changes(self, token: str, roster_changes: Dict[int, Tuple[str, int]]):
        raid = self.raids_resource.get_raid_by_token(token)
        updated_characters = []
        if raid:
            updated_characters = self.raids_resource.update_roster(raid, roster_changes)
        return {'data': [char.to_dict() for char in updated_characters]}
