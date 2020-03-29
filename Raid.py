from pandas import DataFrame
from RaidReader import read_raids
from AttendanceReader import get_standby_count
from Roster import Roster
from datetime import datetime
import math


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
    def upcoming():
        raids = Raid.all_raids()
        today = datetime.now().date()
        raid = min(raids, key=lambda raid: raid.date - today if raid.date >= today else math.inf)
        standby_count = get_standby_count(raid.name, raid.date)
        raid.signees['standby_count'] = raid.signees['name'].map(standby_count)
        print('Following signees do not exist: ' + ', '.join(raid.signees[raid.signees['standby_count'].isnull()]['name']))
        print('Following non-kruisvaarders signed up: ' + ', '.join(raid.signees[~raid.signees['is_kruisvaarder']]['name']))
        return raid

    @staticmethod
    def write_upcoming_roster():
        Raid.upcoming().to_roster().write()

    def __str__(self):
        return f"{self.name}, {self.date}"


if __name__ == '__main__':
    Raid.write_upcoming_roster()
