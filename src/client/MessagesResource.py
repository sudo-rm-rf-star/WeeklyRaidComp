from persistence.TableFactory import TableFactory
from persistence.MessagesTable import MessagesTable
from logic.MessageRef import MessageRef
from typing import Optional
from datetime import datetime


class MessagesResource:
    def __init__(self):
        self.messages_table: MessagesTable = TableFactory().get_messages_table()

    def get_message(self, message_id: int) -> Optional[MessageRef]:
        return self.messages_table.get_message(message_id)

    def create_channel_message(self, message_id: int, guild_id: int, channel_id: int, raid_name: str, raid_datetime: datetime, group_id: int):
        return self.messages_table.create_channel_message(message_id=message_id, guild_id=guild_id,
                                                          channel_id=channel_id, raid_name=raid_name,
                                                          raid_datetime=raid_datetime, group_id=group_id)

    def create_personal_message(self, message_id: int, guild_id: int, user_id: int, raid_name: str, raid_datetime: datetime, group_id: int):
        return self.messages_table.create_personal_message(message_id=message_id, guild_id=guild_id, user_id=user_id,
                                                           raid_name=raid_name, raid_datetime=raid_datetime,
                                                           group_id=group_id)
