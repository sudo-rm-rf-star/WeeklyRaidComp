from datetime import datetime
from typing import Dict, Optional, Any

from logic.enums.Class import Class
from logic.enums.Race import Race
from logic.enums.Role import Role
from logic.enums.RosterStatus import RosterStatus
from logic.enums.SignupStatus import SignupStatus
from typing import List, Tuple


class Character:
    def __init__(self, *, char_name: str, klass: Class, role: Role, race: Race, discord_id: int,
                 created_at: Optional[float] = None,
                 roster_statuses: Optional[List[Tuple[RosterStatus, int]]] = None,
                 signup_statuses: Optional[List[Tuple[SignupStatus, int]]] = None):
        self.name = char_name
        self.klass = klass
        self.role = role
        self.race = race
        self.discord_id = discord_id
        self.roster_statuses = roster_statuses if roster_statuses else []
        self.signup_statuses = signup_statuses if signup_statuses else []
        self.created_at = created_at if created_at else datetime.now().timestamp()

    def set_signup_status(self, signup_status: SignupStatus):
        self.signup_statuses.append((signup_status, int(datetime.now().timestamp())))

    def set_roster_status(self, roster_status: RosterStatus):
        self.roster_statuses.append((roster_status, int(datetime.now().timestamp())))

    def get_signup_status(self) -> SignupStatus:
        if len(self.signup_statuses) > 0:
            return self.signup_statuses[-1][0]
        else:
            return SignupStatus.UNDECIDED

    def get_roster_status(self) -> RosterStatus:
        if len(self.roster_statuses) > 0:
            return self.roster_statuses[-1][0]
        else:
            return RosterStatus.UNDECIDED

    def is_declined(self) -> bool:
        return self.get_signup_status() == SignupStatus.DECLINE and self.get_roster_status() != RosterStatus.ACCEPT

    @staticmethod
    def from_dict(item: Dict[str, Any]):
        return Character(char_name=item['name'],
                         klass=Class[item['class']],
                         role=Role[item['role']],
                         race=Race[item['race']],
                         discord_id=item.get('discord_id', None),
                         signup_statuses=[(SignupStatus[signup_status], timestamp) for
                                          signup_status, timestamp in item.get('signup_statuses', [])],
                         roster_statuses=[(RosterStatus[roster_status], timestamp) for
                                          roster_status, timestamp in item.get('roster_statuses', [])],
                         created_at=item.get('created_at', None))

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'discord_id': self.discord_id,
            'class': self.klass.name,
            'role': self.role.name,
            'race': self.race.name,
            'roster_statuses': [(roster_status.name, timestamp) for roster_status, timestamp in self.roster_statuses],
            'signup_statuses': [(signup_status.name, timestamp) for signup_status, timestamp in self.signup_statuses],
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
