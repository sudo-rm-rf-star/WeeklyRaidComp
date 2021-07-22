from datetime import datetime
from typing import Dict, Optional, Any

from logic.enums.Class import Class
from logic.enums.Role import Role
from logic.enums.RosterStatus import RosterStatus
from logic.enums.SignupStatus import SignupStatus
from typing import List, Tuple


def map_roster_statuses(roster_statuses: List[Tuple]):
    """
    Utility function to add optional team index to roster status
    """
    for roster_status in roster_statuses:
        if len(roster_status) == 2:
            signup_status, timestamp = roster_status
            team_index = 0
        else:
            signup_status, timestamp, team_index = roster_status
        yield signup_status, timestamp, team_index


class Character:
    def __init__(self, *, char_name: str, klass: Class, spec: str, discord_id: int,
                 created_at: Optional[float] = None,
                 roster_statuses: Optional[List[Tuple[RosterStatus, int, int]]] = None,
                 signup_statuses: Optional[List[Tuple[SignupStatus, int]]] = None,
                 realm: str = None, region: str = None):
        self.name = char_name
        self.realm = realm
        self.region = region
        self.klass = klass
        self.spec = spec
        self.discord_id = discord_id
        self.roster_statuses = roster_statuses if roster_statuses else []
        self.signup_statuses = signup_statuses if signup_statuses else []
        self.created_at = created_at if created_at else datetime.now().timestamp()

    def set_signup_status(self, signup_status: SignupStatus):
        self.signup_statuses.append((signup_status, int(datetime.now().timestamp())))

    def set_roster_status(self, roster_status: RosterStatus, team_id: int = 0):
        self.roster_statuses.append((roster_status, int(datetime.now().timestamp()), team_id))

    def get_signup_status(self) -> SignupStatus:
        if len(self.signup_statuses) > 0:
            return self.signup_statuses[-1][0]
        else:
            return SignupStatus.Unknown

    def get_roster_status(self) -> RosterStatus:
        if len(self.roster_statuses) > 0:
            return self.roster_statuses[-1][0]
        else:
            return RosterStatus.Undecided

    def get_team_index(self) -> int:
        if len(self.roster_statuses) > 0:
            return self.roster_statuses[-1][-1]
        else:
            return 0


    def is_declined(self) -> bool:
        return self.get_signup_status() == SignupStatus.Decline and self.get_roster_status() != RosterStatus.Accept

    def get_role(self) -> Role:
        return self.klass.get_role(self.spec)

    @staticmethod
    def from_dict(item: Dict[str, Any]):
        return Character(char_name=item['name'],
                         klass=Class[item['class']],
                         spec=item.get('spec', None),
                         discord_id=item.get('discord_id', None),
                         signup_statuses=[(SignupStatus[signup_status], timestamp) for
                                          signup_status, timestamp in item.get('signup_statuses', [])],
                         roster_statuses=[(RosterStatus[roster_status], timestamp, team_index) for
                                          roster_status, timestamp, team_index in
                                          map_roster_statuses(item.get('roster_statuses', []))],
                         created_at=item.get('created_at', None))

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'discord_id': str(self.discord_id),
            'class': self.klass.name,
            'spec': self.spec,
            'role': self.get_role().name,
            'roster_status': self.get_roster_status().name,
            'team_index': int(self.get_team_index()),
            'signup_status': self.get_signup_status().name,
            'roster_statuses': [(roster_status.name, int(timestamp), int(team_index)) for
                                roster_status, timestamp, team_index in self.roster_statuses],
            'signup_statuses': [(signup_status.name, int(timestamp)) for signup_status, timestamp in
                                self.signup_statuses],
            'created_at': int(self.created_at if self.created_at else datetime.now().timestamp())
        }

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.discord_id == other.discord_id

    def __str__(self) -> str:
        return f'{self.klass.name.capitalize()} {self.name}'

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self):
        return hash((self.name, self.discord_id))
