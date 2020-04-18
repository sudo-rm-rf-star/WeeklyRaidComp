""" Utility class to help for raids with multiple rosters. """
from pandas import DataFrame

from src.common.Constants import signup_choice_to_role_class, player_count
from src.common.Utils import parse_name, now
from src.filehandlers.AttendanceReader import get_standby_count
from src.filehandlers.RosterFileHandler import RosterFileHandler
from src.filehandlers.WhitelistedFileHandler import get_whitelisted
from src.logic.Roster import Roster


class Rosters:
    def __init__(self, raid_name, raid_datetime, rosters, created_at=None, updated_at=None, message_id=None):
        self.rosters = rosters
        self.count = len(rosters)
        self.raid_name = raid_name
        self.raid_datetime = raid_datetime
        self.created_at = now() if not created_at else created_at
        self.updated_at = self.created_at if updated_at is None else updated_at
        self.message_id = message_id

    def set_message_id(self, message_id):
        self.message_id = message_id

    @staticmethod
    def compose(raid):
        roster_count = _roster_count(raid.name)
        signees_per_roster = _get_signees(raid, _roster_count(raid.name))
        rosters = [Roster.compose(raid, signees_per_roster[i]) for i in range(roster_count)]
        return Rosters(raid.name, raid.datetime, rosters)

    @staticmethod
    def load(raid_name, raid_datetime=None):
        rosters = RosterFileHandler().load(raid_name, raid_datetime)

        return Rosters(raid_name=rosters['name'],
                       raid_datetime=rosters['datetime'],
                       created_at=rosters['created_at'],
                       updated_at=rosters['updated_at'],
                       message_id=rosters['message_id'],
                       rosters=[Roster(
                           signees=roster['signees'],
                           accepted=roster['accepted'],
                           bench=roster['bench'],
                           absence=roster['absence'],
                           missing_roles=roster['missing_roles']
                       ) for roster in rosters['rosters']])

    def save(self):
        self.updated_at = now()
        RosterFileHandler().save({
            'name': self.raid_name,
            'datetime': self.raid_datetime,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'message_id': self.message_id,
            'rosters': [
                {
                    'signees': roster.signees,
                    'accepted': roster.accepted,
                    'bench': roster.bench,
                    'absence': roster.absence,
                    'missing_roles': roster.missing_roles,

                } for roster in self.rosters
            ]
        })

    def get(self, i):
        assert i < self.count
        return self.rosters[i]


def _get_signees(raid, roster_count):
    signees = []
    standby_counts = get_standby_count(raid.name, raid.datetime)
    whitelisted = get_whitelisted()

    for signup_choice, chars in raid.signees_per_choice.items():
        for char in chars:
            charname = parse_name(char)
            if signup_choice not in ['Bench', 'Late', 'Absence', 'Tentative']:
                role, clazz = signup_choice_to_role_class[signup_choice]
                player_signup_choice = 'Accepted'
            else:
                player_signup_choice = signup_choice
                role, clazz = None, None

            role = 'dps' if role == 'ranged' or role == 'melee' else role
            roster_status = 'Bench' if signup_choice != 'Absence' else player_signup_choice

            signees.append({'name': charname, 'class': clazz, 'role': role,
                            'signup_choice': player_signup_choice, 'roster_status': roster_status,
                            'whitelisted': charname in whitelisted,
                            'standby_count': standby_counts.get(char, None)})

    signees = DataFrame(signees)
    signees_per_roster = [DataFrame()] * roster_count
    for role, signees_for_role in signees.groupby('role'):
        for clazz, signees_for_clazz_role in signees_for_role.groupby('class'):
            for i, signee in signees_for_clazz_role.iterrows():
                roster_index = i % roster_count
                signees_per_roster[roster_index] = signees_per_roster[roster_index].append(signee, ignore_index=True)
    return signees_per_roster


def _roster_count(raid_name):
    return 2 if player_count[raid_name] == 20 else 1
