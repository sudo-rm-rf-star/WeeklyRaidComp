from typing import Dict, Optional, Any

from logic.enums.Class import Class
from logic.enums.Race import Race
from logic.enums.Role import Role
from logic.enums.RosterStatus import RosterStatus
from logic.enums.SignupStatus import SignupStatus


class Character:
    def __init__(self, *, char_name: str, klass: Class, role: Role, race: Race, discord_id: int, guild_id: int, standby_count: Dict[str, int],
                 roster_status: Optional[RosterStatus] = None,
                 signup_status: Optional[SignupStatus] = None,
                 team_index: Optional[int] = None):
        self.name = char_name
        self.klass = klass
        self.role = role
        self.race = race
        self.discord_id = discord_id
        self.guild_id = guild_id
        self.standby_count = standby_count
        self.roster_status = roster_status if roster_status else RosterStatus.UNDECIDED
        self.signup_status = signup_status if signup_status else SignupStatus.UNDECIDED
        self.team_index = team_index

    def is_declined(self) -> bool:
        return (self.signup_status == SignupStatus.DECLINE and self.roster_status != RosterStatus.ACCEPT) or self.roster_status == RosterStatus.DECLINE

    @staticmethod
    def from_dict(item: Dict[str, Any]):
        return Character(char_name=item['name'],
                         klass=Class[item['class']],
                         role=Role[item['role']],
                         race=Race[item['race']],
                         guild_id=item['guild_id'],
                         discord_id=item.get('discord_id', None),
                         roster_status=RosterStatus[item['roster_status']] if 'roster_status' in item else None,
                         signup_status=SignupStatus[item['signup_status']] if 'signup_status' in item else None,
                         team_index=item.get('team_index', None),
                         standby_count=item['standby_count'])

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'discord_id': self.discord_id,
            'class': self.klass.name,
            'role': self.role.name,
            'race': self.race.name,
            'guild_id': self.guild_id,
            'roster_status': self.roster_status.name,
            'signup_status': self.signup_status.name,
            'team_index': self.team_index,
            'standby_count': self.standby_count
        }

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __str__(self) -> str:
        return f'{self.role.name.capitalize()} {self.klass.name.capitalize()} {self.name}'

    def __hash__(self):
        return hash((self.name, self.discord_id))
