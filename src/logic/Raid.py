from pandas import DataFrame
from src.logic.RaidReader import read_raids
from src.logic.AttendanceReader import get_standby_count
from src.logic.Roster import Roster
from src.common.Constants import pref_per_role
from datetime import datetime
from logging import getLogger


class Raid:
    def __init__(self, name, date, signees):
        self.name = name
        self.date = date
        self.signees = DataFrame(signees)

    def to_roster(self, roster_index=None):
        return Roster.compose(self, roster_index)

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
    def get(name, date=None):
        raids = [raid for raid in Raid.all_raids() if raid.name == name]
        if date:
            date = date.date()
            raids_on_date = [raid for raid in raids if raid.date == date]
            if not len(raids_on_date):
                getLogger().error(f'There are no raids on {date} for {name}.')
                return None
            raid = raids[0]

        else:
            today = datetime.now().date()
            upcoming_raids = [raid for raid in raids if raid.date > today]
            if not len(upcoming_raids):
                getLogger().error(f'There are upcoming raids on {today} for {name}.')
                return None
            raid = min(upcoming_raids, key=lambda raid: raid.date - today)

        standby_count = get_standby_count(raid.name, raid.date)
        raid.signees['standby_count'] = raid.signees['name'].map(standby_count)
        _show_warnings(raid.signees)
        return raid

    @staticmethod
    def write_roster(name, date=None):
        pass

    @staticmethod
    def get_rosters(name, date=None):
        raid = Raid.get(name, date)
        if raid is None:
            return False, None

        raids = [raid]
        if _raid_size(name) == 20:
            raids = raids[0].split_in(2)

        rosters = [raid.to_roster(i) for i, raid in enumerate(raids)]
        return rosters

    def __str__(self):
        return f"{self.name}, {self.date}"


def _raid_size(name):
    return sum(pref_per_role[name].values())


def _show_warnings(signees):
    never_standby = signees[signees['standby_count'].isnull()]['name']
    not_kruisvaarders = signees[~signees['is_kruisvaarder']]['name']
    if len(never_standby) > 0:
        getLogger().warning(f'Following signees do not exist in history: {", ".join(never_standby)}')
    if len(not_kruisvaarders) > 0:
        getLogger().warning(
            f'Following signees are not in the kruisvaarders team: {", ".join(not_kruisvaarders)}')
