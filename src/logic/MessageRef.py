from typing import Optional, Dict, Any
from datetime import datetime


class MessageRef:
    def __init__(self, message_id: int, guild_id: int, group_id: Optional[int] = None, channel_id: Optional[int] = None, user_id: Optional[int] = None,
                 raid_name: Optional[str] = None, raid_datetime: Optional[datetime] = None):
        self.message_id = message_id
        self.channel_id = channel_id
        self.guild_id = guild_id
        self.group_id = group_id
        self.user_id = user_id
        self.raid_name = raid_name
        self.raid_datetime = raid_datetime

    @staticmethod
    def from_dict(item: Dict[str, Any]):
        return MessageRef(message_id=int(item['message_id']),
                          guild_id=int(item['guild_id']),
                          group_id=int(item['group_id']) if item.get('group_id', None) else None,
                          channel_id=int(item['channel_id']) if item.get('channel_id', None) else None,
                          user_id=int(item['user_id']) if item.get('user_id', None) else None,
                          raid_name=item['raid_name'],
                          raid_datetime=datetime.fromtimestamp(float(item['timestamp'])) if 'timestamp' in item else None)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'message_id': str(self.message_id),
            'guild_id': str(self.guild_id),
            'channel_id': str(self.channel_id) if self.channel_id else None,
            'user_id': str(self.user_id) if self.user_id else None,
            'group_id': str(self.group_id) if self.group_id else None,
            'raid_name': self.raid_name if self.raid_name else None,
            'timestamp': str(self.raid_datetime.timestamp())
        }
