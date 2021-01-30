from typing import Dict, Any


class RaidTeam:
    def __init__(self, name: str, group_id: int, events_channel: str, raider_rank: str):
        self.name = name
        self.raider_rank = raider_rank
        self.id = group_id
        self.events_channel = events_channel

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'raider_rank': self.raider_rank,
            'id': str(self.id),
            'events_channel': self.events_channel
        }

    @staticmethod
    def from_dict(item):
        return RaidTeam(
            name=item['name'],
            raider_rank=item['raider_rank'],
            group_id=int(item.get('id', item['group_id'])),
            events_channel=item['events_channel'],
        )
