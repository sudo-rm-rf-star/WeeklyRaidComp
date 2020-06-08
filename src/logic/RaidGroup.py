from typing import Dict, Optional, Any
from utils.Constants import default_num_per_raid_role, default_min_per_raid_role_class, default_max_per_raid_role_class


class RaidGroup:
    def __init__(self,
                 name: str,
                 raider_rank: str,
                 group_id: int,
                 events_channel=str,
                 wl_group_id: Optional[int] = None,
                 num_per_raid_role: Optional[Dict[str, Dict[str, int]]] = None,
                 min_per_raid_role_class: Optional[Dict[str, Dict[str, Dict[str, int]]]] = None,
                 max_per_raid_role_class: Optional[Dict[str, Dict[str, Dict[str, int]]]] = None):
        self.name = name
        self.raider_rank = raider_rank
        self.group_id = group_id
        self.events_channel = events_channel
        self.wl_group_id = wl_group_id
        self.num_per_raid_role = num_per_raid_role if num_per_raid_role else default_num_per_raid_role
        self.min_per_raid_role_class = min_per_raid_role_class if min_per_raid_role_class else default_min_per_raid_role_class
        self.max_per_raid_role_class = max_per_raid_role_class if max_per_raid_role_class else default_max_per_raid_role_class

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'raider_rank': self.raider_rank,
            'group_id': self.group_id,
            'events_channel': self.events_channel,
            'wl_group_id': self.wl_group_id,
            'num_per_raid_role': self.num_per_raid_role,
            'min_per_raid_role_class': self.min_per_raid_role_class,
            'max_per_raid_role_class': self.max_per_raid_role_class
        }

    @staticmethod
    def from_dict(item):
        return RaidGroup(
            name=item['name'],
            raider_rank=item['raider_rank'],
            group_id=item['group_id'],
            events_channel=item['events_channel'],
            wl_group_id=item.get('wl_group_id'),
            num_per_raid_role=item.get('num_per_raid_role'),
            min_per_raid_role_class=item.get('min_per_raid_role_class'),
            max_per_raid_role_class=item.get('max_per_raid_role_class')
        )


