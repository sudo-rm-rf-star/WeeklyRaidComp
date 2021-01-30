from datetime import datetime
from typing import Dict, Optional, Any

from logic.enums.Class import Class
from logic.enums.Race import Race
from logic.enums.Role import Role
from logic.enums.RosterStatus import RosterStatus
from logic.enums.SignupStatus import SignupStatus


class Character:
    def __init__(self, *, char_name: str, klass: Class, role: Role, race: Race, discord_id: int, created_at: float,
                 roster_status: Optional[RosterStatus] = None,
                 signup_status: Optional[SignupStatus] = None):
        self.name = char_name
        self.klass = klass
        self.role = role
        self.race = race
        self.discord_id = discord_id
        self.roster_status = roster_status if roster_status else RosterStatus.UNDECIDED
        self.signup_status = signup_status if signup_status else SignupStatus.UNDECIDED
        self.created_at = created_at

    def is_declined(self) -> bool:
        return self.signup_status == SignupStatus.DECLINE and self.roster_status != RosterStatus.ACCEPT

    @staticmethod
    def from_dict(item: Dict[str, Any]):
        return Character(char_name=item['name'],
                         klass=Class[item['class']],
                         role=Role[item['role']],
                         race=Race[item['race']],
                         discord_id=item.get('discord_id', None),
                         roster_status=RosterStatus[item['roster_status']] if 'roster_status' in item else None,
                         signup_status=SignupStatus[item['signup_status']] if 'signup_status' in item else None,
                         created_at=item.get('created_at', None))

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'discord_id': self.discord_id,
            'class': self.klass.name,
            'role': self.role.name,
            'race': self.race.name,
            'roster_status': self.roster_status.name,
            'signup_status': self.signup_status.name,
            'created_at': int(self.created_at if self.created_at else datetime.now().timestamp())
        }

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.discord_id == other.discord_id

    def __str__(self) -> str:
        return f'{self.role.name.capitalize()} {self.klass.name.capitalize()} {self.name}'

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self):
        return hash((self.name, self.discord_id))
