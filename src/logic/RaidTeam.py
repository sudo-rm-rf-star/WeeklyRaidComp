from typing import Dict, Any


class RaidTeam:
    def __init__(self, team_name: str, guild_id: int, realm: str, region: str, officer_rank: str,
                 raider_rank: str, events_channel: str, logs_channel: str):
        self.name = team_name
        self.guild_id = guild_id
        self.realm = realm
        self.region = region
        self.raider_rank = raider_rank
        self.officer_rank = officer_rank
        self.events_channel = events_channel
        self.logs_channel = logs_channel

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict[str, Any]:
        return {
            'team_name': self.name,
            'guild_id': str(self.guild_id),
            'realm': self.realm,
            'region': self.region,
            'officer_rank': self.officer_rank,
            'raider_rank': self.raider_rank,
            'logs_channel': self.logs_channel,
            'events_channel': self.events_channel
        }

    @staticmethod
    def from_dict(item):
        return RaidTeam(
            team_name=item['team_name'],
            guild_id=int(item['guild_id']),
            region=item['region'],
            realm=item['realm'],
            raider_rank=item['raider_rank'],
            officer_rank=item['officer_rank'],
            events_channel=item['events_channel'],
            logs_channel=item['logs_channel']
        )
