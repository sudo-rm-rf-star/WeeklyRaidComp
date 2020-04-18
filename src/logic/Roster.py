from pandas import DataFrame
from src.common.Constants import pref_per_role, min_per_class_role, max_per_class_role, VERBOSE, ROSTER_STORAGE, \
    DATE_FORMAT, abbrev_to_full
from collections import defaultdict
import os
import json
from datetime import datetime


class Roster:
    def __init__(self, raid_name, raid_date, signees, accepted, bench, absence, missing_roles, created_at=None,
                 updated_at=None,
                 roster_index=None):
        self.raid_name = raid_name
        self.raid_date = raid_date
        self.signees = signees
        self.accepted = accepted
        self.bench = bench
        self.absence = absence
        self.missing_roles = missing_roles
        self.index = roster_index
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if created_at is None else created_at
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
        return f"{abbrev_to_full[self.raid_name]} ({self.raid_date})"

    @staticmethod
    def compose(raid, roster_index=None):
        signees = DataFrame(raid.signees)
        signees.loc[signees['signup_status'] == 'Absence', 'roster_status'] = 'Absence'
        signees.loc[signees['signup_status'] != 'Absence', 'roster_status'] = 'Bench'
        signees.loc[signees['role'] == 'ranged', 'role'] = 'dps'
        signees.loc[signees['role'] == 'melee', 'role'] = 'dps'
        missing_roles = {}

        def eligible():
            return signees[(signees['is_kruisvaarder'] == 1) & (signees['signup_status'] == 'Accepted')]

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
        return Roster(raid.name, raid.date, raid.signees['name'].tolist(), accepted, bench, absence, missing_roles,
                      roster_index)

    def save(self):
        with _open_roster_file(self.raid_name, self.raid_date) as out_file:
            out_file.write(json.dumps({
                'name': self.raid_name,
                'date': self.raid_date,
                'signees': self.signees,
                'accepted': self.accepted,
                'bench': self.bench,
                'absence': self.absence,
                'missing_roles': self.missing_roles,
                'created_at': self.created_at,
                'updated_at': self.updated_at,
                'index': self.index
            }))

    @staticmethod
    def load(raid_name, raid_date=None):
        if raid_date is None:
            raid_date = upcoming_date(raid_name)

        roster = json.loads(_open_roster_file(raid_name, raid_date, mode='w+').read())
        return Roster(roster['name'], roster['date'], roster['signees'], roster['accepted'], roster['bench'],
                      roster['absence'], roster['missing_roles'], roster['created_at'], roster['updated_at'],
                      roster['index'])


def _open_roster_file(raid_name, raid_date, mode='r'):
    return open(os.path.join(ROSTER_STORAGE, f'{raid_name}_{raid_date.strftime(fmt=DATE_FORMAT)}.csv'), mode=mode,
                encoding='utf-8')


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


def all_raid_dates():
    return [tuple(file.split('_')) for file in os.listdir(ROSTER_STORAGE)]


def upcoming_raid_dates():
    raid_dates = [(name, datetime.strptime(date, DATE_FORMAT)) for name, date in all_raid_dates()]
    return [(name, date.strftime(DATE_FORMAT)) for name, date in raid_dates if date.date() > datetime.now().date()]


def upcoming_date(raid_name):
    return min([date for name, date in upcoming_raid_dates() if name == raid_name.lower()], key=lambda x: datetime.strptime(x[1], DATE_FORMAT))
