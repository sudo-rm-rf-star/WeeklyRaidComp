from typing import Dict, Any


class RaidTeam:
    def __init__(self, team_name: str, guild_id: int, realm: str, region: str, manager_ids: list, raider_ids: list,
                 events_channel: str, manager_channel: str, logs_channel: str):
        self.name = team_name
        self.guild_id = guild_id
        self.realm = realm
        self.region = region
        self.manager_ids = list(set(manager_ids))
        self.raider_ids = list(set(raider_ids))
        self.events_channel = events_channel
        self.manager_channel = manager_channel
        self.logs_channel = logs_channel

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict[str, Any]:
        return {
            'team_name': self.name,
            'guild_id': str(self.guild_id),
            'realm': self.realm,
            'region': self.region,
            'manager_ids': self.manager_ids,
            'raider_ids': self.raider_ids,
            'logs_channel': self.logs_channel,
            'events_channel': self.events_channel,
            'manager_channel': self.manager_channel
        }

    @staticmethod
    def from_dict(item):
        return RaidTeam(
            team_name=item['team_name'],
            guild_id=int(item['guild_id']),
            region=item['region'],
            realm=item['realm'],
            raider_ids=list(item['raider_ids']),
            manager_ids=list(item['manager_ids']),
            events_channel=item['events_channel'],
            manager_channel=item['manager_channel'],
            logs_channel=item['logs_channel']
        )
