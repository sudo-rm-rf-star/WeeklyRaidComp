from collections import defaultdict

from src.client.entities.RaidNotification import RaidNotification
from src.filehandlers.RaidFileHandler import load_raid_events, save_raid_events
from src.exceptions.EventDoesNotExistException import EventDoesNotExistException
from src.time.DateOptionalTime import DateOptionalTime
from src.logic.RaidEvent import RaidEvent
from src.client.GuildClient import GuildClient
from src.client.entities.RaidMessage import RaidMessage
from typing import Any
import discord


class RaidEvents:
    class __RaidEvents:
        def __init__(self):
            self.raids_by_name_and_datetime = defaultdict(dict)
            self.raids_by_message_id = {}
            for raid in load_raid_events():
                self.add(raid)

        def create(self, raid_name, raid_datetime):
            raid_event = RaidEvent(raid_name, raid_datetime)
            self.add(raid_event)
            return raid_event

        async def remove(self, client: GuildClient, raid_event: RaidEvent) -> None:
            assert self.exists(raid_event.name, raid_event.datetime)
            for message_id, _, _ in raid_event.message_id_pairs:
                del self.raids_by_message_id[message_id]
            del self.raids_by_name_and_datetime[raid_event.name][raid_event.datetime]
            await RaidMessage(client, raid_event).remove()

        def add(self, raid_event: RaidEvent) -> None:
            if raid_event.datetime not in self.raids_by_name_and_datetime[raid_event.name]:
                self.raids_by_name_and_datetime[raid_event.name][raid_event.datetime] = raid_event
                for (message_id, _, _) in raid_event.message_id_pairs:
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

        def get_raid_for_message(self, message_id: str) -> RaidEvent:
            return self.raids_by_message_id.get(message_id, None)

        def get_raid_for_notification(self, message_id: str) -> RaidEvent:
            return self.raids_by_message_id.get(message_id, None)

        def add_raid_message(self, message_id: str, recipient_id: str, message_type: type, raid_event: RaidEvent):
            self.raids_by_message_id[message_id] = raid_event
            raid_event.message_id_pairs.add((message_id, recipient_id, message_type))

        def store(self):
            save_raid_events([raid for raids in self.raids_by_name_and_datetime.values() for raid in raids.values()])

        async def send_raid_notification(self, client: GuildClient, recipient: discord.Member, raid_event: RaidEvent) -> None:
            msg = await RaidNotification(client, raid_event).send_to(recipient)
            self.add_raid_message(msg.id, recipient.id, RaidNotification, raid_event)

        async def send_raid_message(self, client: GuildClient, recipient: discord.TextChannel, raid_event: RaidEvent) -> None:
            msg = await RaidMessage(client, raid_event).send_to(recipient)
            self.add_raid_message(msg.id, recipient.id, RaidMessage, raid_event)

    instance = None

    def __new__(cls):
        if not RaidEvents.instance:
            RaidEvents.instance = RaidEvents.__RaidEvents()
        return RaidEvents.instance

    def __getattr__(self, name: str) -> Any:
        return getattr(self.instance, name)

    def __setattr__(self, name: str, **kwargs) -> None:
        return setattr(self.instance, name, **kwargs)
