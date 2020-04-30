from collections import defaultdict
from src.filehandlers.RaidFileHandler import load_raid_events, save_raid_events
from src.exceptions.EventDoesNotExistException import EventDoesNotExistException
from src.time.DateOptionalTime import DateOptionalTime
from src.logic.RaidEvent import RaidEvent
from typing import Any


class RaidEvents:
    class __RaidEvents:
        def __init__(self):
            self.raids_by_name_and_datetime = defaultdict(dict)
            self.raids_by_message_id = {}
            for raid in load_raid_events():
                self.add(raid)

        def add(self, raid_event: RaidEvent) -> None:
            if raid_event.datetime not in self.raids_by_name_and_datetime[raid_event.name]:
                self.raids_by_name_and_datetime[raid_event.name][raid_event.datetime] = raid_event
                for (message_id, channel_id) in raid_event.message_id_pairs:
                    self.raids_by_message_id[message_id] = raid_event

        def exists(self, raid_name: str, raid_datetime=None) -> bool:
            try:
                self.get(raid_name, raid_datetime)
                return True
            except EventDoesNotExistException:
                return False

        def get(self, raid_name: str, raid_datetime=None) -> RaidEvent:
            if raid_name not in self.raids_by_name_and_datetime:
                raise EventDoesNotExistException(f"There are no events for raid {raid_name}")

            if raid_datetime is None:
                upcoming_raid_datetimes = [raid_datetime for raid_datetime in self.raids_by_name_and_datetime[raid_name].keys()
                                           if raid_datetime >= DateOptionalTime.now()]
                if len(upcoming_raid_datetimes) == 0:
                    raise EventDoesNotExistException(f"Could not find any upcoming event for {raid_name}")
                raid_datetime = min(upcoming_raid_datetimes)

            if raid_datetime not in self.raids_by_name_and_datetime[raid_name]:
                raise EventDoesNotExistException(f"No events for raid {raid_name} on date {raid_datetime}")

            return self.raids_by_name_and_datetime[raid_name][raid_datetime]

        def store(self):
            save_raid_events([raid for raids in self.raids_by_name_and_datetime.values() for raid in raids.values()])

        def get_by_message_id(self, message_id: str) -> RaidEvent:
            return self.raids_by_message_id.get(message_id, None)

    instance = None

    def __new__(cls):
        if not RaidEvents.instance:
            RaidEvents.instance = RaidEvents.__RaidEvents()
        return RaidEvents.instance

    def __getattr__(self, name: str) -> Any:
        return getattr(self.instance, name)

    def __setattr__(self, name: str, **kwargs) -> None:
        return setattr(self.instance, name, **kwargs)
