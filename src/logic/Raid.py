from src.filehandlers.RaidFileHandler import RaidFileHandler


class Raid:
    def __init__(self, name, raid_datetime, signees_per_choice):
        self.name = name
        self.datetime = raid_datetime
        self.signees_per_choice = signees_per_choice

    def signees(self):
        return [signee for signees in self.signees_per_choice.values() for signee in signees]

    @staticmethod
    def load(raid_name, raid_datetime=None):
        raid = RaidFileHandler().load(raid_name, raid_datetime)
        return Raid(raid['name'], raid['datetime'], raid['signees'])

    @staticmethod
    def load_all():
        return [Raid(raid['name'], raid['datetime'], raid['signees']) for raid in RaidFileHandler().load_all()]

    def save(self):
        RaidFileHandler().save({
            'name': self.name,
            'datetime': self.datetime,
            'signees': self.signees_per_choice,
        })

    def get_date(self):
        return self.datetime.date()

    def get_time(self):
        return self.datetime.time()

    def get_weekday(self):
        return self.datetime.weekday()

    def get_signees_per_choice(self):
        return self.signees_per_choice

    def get_choice_per_signee(self):
        signees = {}
        for choice, signees_for_choice in self.get_signees_per_choice().items():
            for signee in signees_for_choice:
                signees[signee] = choice
        return signees
