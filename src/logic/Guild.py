from typing import Dict, Optional, Any, List
from logic.RaidGroup import RaidGroup


class Guild:
    def __init__(self, name: str, realm: str, region: str, manager_rank: str, guild_id: Optional[int],
                 wl_guild_id: Optional[int] = None, groups: Optional[List[RaidGroup]] = None,
                 logs_channel: Optional[str] = None):
        self.name = name
        self.manager_rank = manager_rank
        self.realm = realm
        self.region = region
        self.guild_id = guild_id
        self.wl_guild_id = wl_guild_id
        self.raid_groups = groups if groups else []
        self.logs_channel = logs_channel
        if wl_guild_id is None:
            from utils.WarcraftLogs import get_wl_guild_id
            self.wl_guild_id = get_wl_guild_id(guild=name, region=region, realm=realm)
        else:
            self.wl_guild_id = wl_guild_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'manager_rank': self.manager_rank,
            'realm': self.realm,
            'region': self.region,
            'guild_id': str(self.guild_id),
            'wl_guild_id': self.wl_guild_id,
            'groups': [group.to_dict() for group in self.raid_groups],
            'logs_channel': self.logs_channel,
        }

    @staticmethod
    def from_dict(item):
        return Guild(
            name=item['name'],
            realm=item['realm'],
            region=item.get('region', 'Europe'),  # TODO remove me for region expansion
            manager_rank=item['manager_rank'],
            guild_id=int(item.get('guild_id')),
            wl_guild_id=item.get('wl_guild_id'),
            groups=[RaidGroup.from_dict(team) for team in item['groups']] if 'groups' in item else None,
            logs_channel=item.get('logs_channel'),
        )


