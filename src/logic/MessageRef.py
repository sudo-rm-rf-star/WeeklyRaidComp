from typing import Optional, Dict, Any
from datetime import datetime
import json


class MessageRef:
    def __init__(self, message_id: int, guild_id: int, team_name: Optional[str] = None,
                 channel_id: Optional[int] = None, user_id: Optional[int] = None, raid_name: Optional[str] = None,
                 raid_datetime: Optional[datetime] = None, **kwargs):
        self.message_id = message_id
        self.channel_id = channel_id
        self.guild_id = guild_id
        self.team_name = team_name
        self.user_id = user_id
        self.raid_name = raid_name
        self.raid_datetime = raid_datetime
        self.kwargs = kwargs

    @staticmethod
    def from_dict(item: Dict[str, Any]):
        return MessageRef(message_id=int(item['message_id']),
                          guild_id=int(item['guild_id']),
                          team_name=item['team_name'],
                          channel_id=int(item['channel_id']) if item.get('channel_id', None) else None,
                          user_id=int(item['user_id']) if item.get('user_id', None) else None,
                          raid_name=item['raid_name'],
                          raid_datetime=datetime.fromtimestamp(float(item['timestamp'])) if 'timestamp' in item else None,
                          **json.loads(item.get('kwargs', json.dumps({}))))

    def to_dict(self) -> Dict[str, Any]:
        return {
            'message_id': str(self.message_id),
            'guild_id': str(self.guild_id),
            'channel_id': str(self.channel_id) if self.channel_id else None,
            'user_id': str(self.user_id) if self.user_id else None,
            'team_name': str(self.team_name) if self.team_name else None,
            'raid_name': self.raid_name if self.raid_name else None,
            'timestamp': str(self.raid_datetime.timestamp()),
            'kwargs': json.dumps(self.kwargs)
        }
