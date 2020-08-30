from typing import Dict, Optional, Any, List
from datetime import datetime
from logic.RaidGroup import RaidGroup


class Guild:
    def __init__(self, name: str, realm: str, manager_rank: str, guild_id: Optional[int], wl_guild_id: Optional[int], groups: Optional[List[RaidGroup]] = None,
                 logs_channel: Optional[str] = None, do_not_scan_before: Optional[datetime] = None):
        self.name = name
        self.manager_rank = manager_rank
        self.realm = realm
        self.guild_id = guild_id
        self.wl_guild_id = wl_guild_id
        self.raid_groups = groups if groups else []
        self.logs_channel = logs_channel
        self.do_not_scan_before = do_not_scan_before

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'manager_rank': self.manager_rank,
            'realm': self.realm,
            'guild_id': str(self.guild_id),
            'wl_guild_id': self.wl_guild_id,
            'groups': [group.to_dict() for group in self.raid_groups],
            'logs_channel': self.logs_channel,
            'do_not_scan_wl_before': int(self.do_not_scan_before.timestamp()) if self.do_not_scan_before else None
        }

    @staticmethod
    def from_dict(item):
        return Guild(
            name=item['name'],
            realm=item['realm'],
            manager_rank=item['manager_rank'],
            guild_id=int(item.get('guild_id')),
            wl_guild_id=item.get('wl_guild_id'),
            groups=[RaidGroup.from_dict(team) for team in item['groups']] if 'groups' in item else None,
            logs_channel=item.get('logs_channel'),
            do_not_scan_before=datetime.fromtimestamp(item['do_not_scan_before']) if 'do_not_scan_before' in item else None
        )


