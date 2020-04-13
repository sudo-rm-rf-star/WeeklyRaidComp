from pandas import DataFrame, concat
from RaidReader import read_raids
from AttendanceReader import get_standby_count
from RosterWriter import RosterWriter
from Roster import Roster
from datetime import datetime
from Constant import pref_per_role
import sys


class Raid:
    def __init__(self, name, date, signees):
        self.name = name
        self.date = date
        self.signees = DataFrame(signees)

    def to_roster(self):
        return Roster.compose(self)

    @staticmethod
    def all_raids():
        return [Raid(tpl[0], tpl[1], tpl[2]) for tpl in read_raids()]

    # Split raid into k equally sized raids based on class-roles.
    def split_in(self, k):
        raids = [DataFrame() for _ in range(k)]
        for role, signees_for_role in self.signees.groupby('role'):
            for clazz, signees_for_clazz_role in signees_for_role.groupby('class'):
                for i, signee in signees_for_clazz_role.iterrows():
                    raid_index = i % k
                    raids[raid_index] = raids[raid_index].append(signee, ignore_index=True)
        return [Raid(self.name, self.date, raid) for raid in raids]

    @staticmethod
    def upcoming(name):
        raids = [raid for raid in Raid.all_raids() if raid.name == name]
        today = datetime.now().date()
        upcoming_raids = [raid for raid in raids if raid.date > today]
        raid = min(upcoming_raids, key=lambda raid: raid.date - today)
        print(f'Making raid for {raid.name} at {raid.date}')
        standby_count = get_standby_count(raid.name, raid.date)
        raid.signees['standby_count'] = raid.signees['name'].map(standby_count)
        print('Following signees do not exist in history: ' + ', '.join(
            raid.signees[raid.signees['standby_count'].isnull()]['name']))
        print('Following non-kruisvaarders signed up: ' + ', '.join(
            raid.signees[~raid.signees['is_kruisvaarder']]['name']))
        return raid

    @staticmethod
    def write_upcoming_roster(name):
        raids = [Raid.upcoming(name)]
        if _raid_size(name) == 20:
            raids = raids[0].split_in(2)

        rosters = [raid.to_roster() for raid in raids]
        RosterWriter(raid_name, raids[0].date).write_rosters(rosters)

    def __str__(self):
        return f"{self.name}, {self.date}"


def _raid_size(name):
    return sum(pref_per_role[name].values())


if __name__ == '__main__':
    raid_name = sys.argv[1]
    Raid.write_upcoming_roster(raid_name)
