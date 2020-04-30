class Player:
    def __init__(self, discord_id, char_name, klass, role, race, present_dates=None, standby_dates=None):
        self.discord_id = discord_id
        self.name = char_name
        self.klass = klass
        self.role = role
        self.race = race
        # These are based only on historical data
        self.present_dates = {} if not present_dates else present_dates
        self.standby_dates = {} if not standby_dates else standby_dates

    def add_standby_date(self, raid_name, raid_datetime):
        if raid_name not in self.standby_dates:
            self.standby_dates[raid_name] = set()
        self.standby_dates[raid_name].add(raid_datetime)

    def add_present_date(self, raid_name, raid_datetime):
        if raid_name not in self.present_dates:
            self.present_dates[raid_name] = set()
        self.present_dates[raid_name].add(raid_datetime)

    def get_standby_dates(self, raid_name):
        return self.standby_dates.get(raid_name, set())

    def get_standby_count(self, raid_name):
        return len(self.get_standby_dates(raid_name))

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return f'{self.role} {self.klass} {self.name}'

