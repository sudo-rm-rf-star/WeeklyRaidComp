from collections import defaultdict
from pandas import DataFrame

from src.filehandlers.AttendanceReader import get_standby_count
from src.filehandlers.RosterFileHandler import RosterFileHandler
from src.filehandlers.WhitelistedFileHandler import get_whitelisted
from src.common.Constants import pref_per_role, min_per_class_role, max_per_class_role, VERBOSE, abbrev_to_full, \
    signup_choice_to_role_class, player_count
from src.common.Utils import parse_name, now


class Roster:
    def __init__(self, raid_name, raid_datetime, signees, accepted, bench, absence, missing_roles, created_at=None,
                 updated_at=None,
                 index=None):
        self.raid_name = raid_name
        self.raid_datetime = raid_datetime
        self.signees = signees
        self.accepted = accepted
        self.bench = bench
        self.absence = absence
        self.missing_roles = missing_roles
        self.index = index
        self.created_at = now() if not created_at else created_at
        self.updated_at = self.created_at if updated_at is None else updated_at

    def accept_player(self, player):
        success = True
        if player not in self.signees:
            success = False
            message = f"{player} did not accepted the raid event. I cannot add him to the roster. " \
                      f"Add {player} to the raid composition as follows: !addUser [eventID] [ClassRole] {player}. " \
                      f"Contact Dok for further information."
        else:
            if player in self.accepted:
                success = False
                message = f"Player {player} is already accepted"
            elif player in self.bench:
                self.bench.remove(player)
                message = f"Moved {player} from bench to accepted"
            elif player in self.absence:
                self.absence.remove(player)
                message = f"Moved {player} from Accepted to Absence"
            else:
                message = f"Player {player} is now accepted"
        if success:
            self.accepted.append(player)

        return success, f"{message} - {self}"

    def bench_player(self, player):
        success = True

        if player in self.accepted:
            self.accepted.remove(player)
            message = f"Moved {player} from accepted to bench"
        elif player in self.bench:
            success = False
            message = f"Player {player} is already benched"
        elif player in self.absence:
            self.absence.remove(player)
            message = f"Moved {player} from absent to bench"
        else:
            assert player not in self.signees
            message = f"{player} did not sign up. He is now benched."

        if success:
            self.bench.append(player)

        return success, f"{message} - {self}"

    def remove_player(self, player):
        success = True
        if player in self.accepted:
            self.accepted.remove(player)
            message = f"Removed {player} from accepted"
        elif player in self.bench:
            self.bench.remove(player)
            message = f"Removed {player} from benched"
        elif player in self.absence:
            message = f"Removed {player} from absence"
            self.absence.remove(player)
        else:
            success = False
            message = f"Could not find {player}"

        return success, f"{message} - {self}"

    def __str__(self):
        return f"{abbrev_to_full[self.raid_name]} ({self.raid_datetime})"

    @staticmethod
    def compose(raid):
        roster_count = 2 if player_count[raid.name] == 20 else 1
        signees_per_roster = _get_signees(raid, roster_count)
        return [_compose_roster(raid, signees_per_roster[i], i) for i in range(roster_count)]

    def load(self, raid_name, raid_datetime=None):
        roster = RosterFileHandler().load(raid_name, raid_datetime)
        return Roster(raid_name=roster['name'],
                      raid_datetime=roster['datetime'],
                      signees=roster['signees'],
                      accepted=roster['accepted'],
                      bench=roster['bench'],
                      absence=roster['absence'],
                      missing_roles=roster['missing_roles'],
                      created_at=roster['created_at'],
                      updated_at=roster['updated_at'],
                      index=roster['index'])

    def save(self):
        self.updated_at = now()
        RosterFileHandler().save({
            'name': self.raid_name,
            'datetime': self.raid_datetime,
            'signees': self.signees,
            'accepted': self.accepted,
            'bench': self.bench,
            'absence': self.absence,
            'missing_roles': self.missing_roles,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'index': self.index
        })


def _calculate_importance(cur, mini, maxi):
    maxi = max(maxi, cur)
    mini = min(mini - 1, cur)
    cur = max(mini, cur)
    return 1 - (cur - mini) / (maxi - mini)


def _chars_per_status(signees):
    records = signees.sort_values(by='class').to_dict(orient='records')
    status_to_char = defaultdict(list)
    for record in records:
        status_to_char[record['roster_status']].append(record['name'])
    return status_to_char


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


def _compose_roster(raid, signees, roster_index=None):
    missing_roles = {}

    def eligible():
        return signees[(signees['whitelisted'] == 1) & (signees['signup_choice'] == 'Accepted')]

    for role, signees_for_role in eligible().groupby('role'):
        for clazz, signees_for_class in signees_for_role.groupby("class"):
            for i, (j, signee) in enumerate(
                    signees_for_class.sort_values('standby_count', ascending=False).iterrows()):
                score = _calculate_importance(i, min_per_class_role[raid.name][role][clazz],
                                              max_per_class_role[raid.name][role][clazz])
                signees.at[j, "score"] = score

    for role, signees_for_role in eligible().groupby('role'):
        lowest_standby_loc = signees_for_role.sort_values('standby_count', ascending=True).head(n=1).index[0]
        signees.at[lowest_standby_loc, 'score'] = -1
        if VERBOSE:
            print(signees_for_role.sort_values('standby_count', ascending=True).head(n=3))

    for role, signees_for_role in eligible().groupby('role'):
        pref_count = pref_per_role[raid.name][role]
        accepted_for_role = signees_for_role.sort_values('score', ascending=False).iloc[:pref_count]
        accepted_count = accepted_for_role.shape[0]
        if accepted_count < pref_count:
            missing_roles[role] = pref_count - accepted_count
        for j, accepted_signee in accepted_for_role.iterrows():
            signees.at[j, "roster_status"] = 'Accepted'

    chars_per_status = _chars_per_status(signees)
    accepted = chars_per_status['Accepted']
    bench = chars_per_status['Bench']
    absence = chars_per_status['Absence']
    return Roster(raid_name=raid.name,
                  raid_datetime=raid.datetime,
                  signees=raid.signees(),
                  accepted=accepted,
                  bench=bench,
                  absence=absence,
                  missing_roles=missing_roles,
                  index=roster_index)
