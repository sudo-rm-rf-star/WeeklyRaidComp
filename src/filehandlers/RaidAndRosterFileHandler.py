"""This file has a tight correlation with Roster and Raid filenames"""
import os
import json
from datetime import datetime, date
from src.common.Constants import FILE_DATETIME_FORMAT, STORAGE_SUFFIX
from src.common.Utils import from_datetime, to_datetime
from src.exceptions.EventDoesNotExistException import EventDoesNotExistException
from src.exceptions.InvalidArgumentException import InvalidArgumentException


class RaidAndRosterFileHandler:
    def __init__(self, dirr):
        self.dir = dirr

    def all_raid_datetimes(self):
        filename_tuples = [tuple(file.rstrip(STORAGE_SUFFIX).split('_')) for file in os.listdir(self.dir)]
        return [(tpl[0], datetime.strptime('_'.join(tpl[1:]), FILE_DATETIME_FORMAT)) for tpl in filename_tuples]

    def upcoming_raid_datetimes(self):
        return [(raid_name, raid_datetime) for raid_name, raid_datetime in self.all_raid_datetimes()
                if raid_datetime.date() > datetime.now().date()]

    def upcoming_datetime(self, name_arg, datetime_arg):
        try:
            raid_datetimes = [raid_datetime for raid_name, raid_datetime in self.upcoming_raid_datetimes() if
                              raid_name == name_arg.lower()]
            if isinstance(datetime_arg, date):
                raid_datetimes = [raid_datetime for raid_datetime in raid_datetimes if
                                  raid_datetime.date() == datetime_arg]
                if len(raid_datetimes) == 2:
                    raise InvalidArgumentException(f'There are two raids for {name_arg} on {datetime_arg}. Please specify time.')
            return min(raid_datetimes)
        except ValueError:
            raise EventDoesNotExistException(f'Could not find any upcoming raids for {name_arg}')

    def load(self, raid_name, raid_datetime=None, file_index=None):
        if raid_datetime is None or isinstance(raid_datetime, date) and not isinstance(raid_datetime, datetime):
            raid_datetime = self.upcoming_datetime(raid_name, raid_datetime)
        rs_dict = json.load(self._open_file(raid_name, raid_datetime, mode='r'))
        rs_dict['datetime'] = to_datetime(rs_dict['datetime'])
        return rs_dict

    def load_all(self):
        return [self.load(raid_name, raid_datetime) for raid_name, raid_datetime in self.all_raid_datetimes()]

    def save(self, rs_dict, file_index=None):
        raid_datetime = rs_dict['datetime']
        rs_dict['datetime'] = from_datetime(raid_datetime)
        with self._open_file(rs_dict['name'], raid_datetime, mode='w+') as file:
            json.dump(rs_dict, file)

    def _open_file(self, raid_name, raid_datetime, mode='r', file_index=''):
        try:
            file_index = '_' + file_index if file_index else ''
            return open(os.path.join(self.dir, f'{raid_name}_{raid_datetime.strftime(FILE_DATETIME_FORMAT)}{str(file_index)}{STORAGE_SUFFIX}'),
                        mode=mode,
                        encoding='utf-8')
        except FileNotFoundError:
            raise EventDoesNotExistException(f'Could not find {raid_name} on {raid_datetime}.')
