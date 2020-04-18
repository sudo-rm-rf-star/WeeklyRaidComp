import os
import json
from collections import defaultdict
from src.common.Constants import raid_abbrev_short
from src.common.Constants import RAID_STORAGE
from src.common.Utils import parse_date


class RaidHelperMessage:
    def __init__(self, message):
        self.fields = [field.value for embed in message.embeds for field in embed.fields]
        self.message = message

    def get_title_field(self):
        return self.fields[0]

    def get_date_field(self):
        return self.fields[3]

    def get_time_field(self):
        return self.fields[4]

    def get_time(self):
        return self.get_time_field().split('[')[1].split('**')[1]

    def get_date(self):
        return self.get_date_field().split(']')[0].split('[')[-1]

    def get_weekday(self):
        return parse_date(self.get_date()).weekday()

    def get_title(self):
        return ''.join([chars[-1] for chars in self.get_title_field().split('_')][:-1])

    def get_short_title(self):
        title = self.get_title()
        return raid_abbrev_short.get(title, title)

    def get_signees_per_choice(self):
        signees = defaultdict(list)
        accepted_i = 5
        other_i = 15

        for row in self.fields[accepted_i:other_i]:
            for entry in row.splitlines()[1:]:
                cols = entry.split(' ')
                signup_choice = cols[0].split(':')[1]
                charname = cols[-1].split('**')[1]
                signees[signup_choice].append(charname)

        for entry in self.fields[other_i].splitlines()[1:]:
            signup_choice = entry.split(':')[1]
            for charname in entry.split('**')[1::2]:
                signees[signup_choice].append(charname)

        return signees

    def get_choice_per_signee(self):
        signees = {}
        for choice, signees_for_choice in self.get_signees_per_choice().items():
            for signee in signees_for_choice:
                signees[signee] = choice
        return signees

    def save(self):
        title = self.get_short_title()
        date = self.get_date()
        signees = self.get_signees_per_choice()
        with open(os.path.join(RAID_STORAGE, f'{title}_{date}.csv'), 'w+') as out_file:
            out_file.write(json.dumps({
                'name': title,
                'date': date,
                'signees': signees
            }))
