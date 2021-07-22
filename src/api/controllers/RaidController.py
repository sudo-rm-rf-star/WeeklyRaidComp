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
        self.event_queue.send_event(RosterUpdated(token, roster_changes))
        return {'data': "PROCESSING"}
