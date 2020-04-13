from pandas import DataFrame
from RaidReader import read_raids
from AttendanceReader import get_standby_count
from Roster import Roster
from datetime import datetime
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
        raid = Raid.upcoming(name)
        raid.to_roster().write(raid.name, raid.date)

    def __str__(self):
        return f"{self.name}, {self.date}"


if __name__ == '__main__':
    raid_name = sys.argv[1]
    Raid.write_upcoming_roster(raid_name)
