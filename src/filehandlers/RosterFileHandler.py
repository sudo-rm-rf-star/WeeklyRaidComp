from src.filehandlers.RaidAndRosterFileHandler import RaidAndRosterFileHandler
from src.common.Constants import ROSTER_STORAGE, DATETIMESEC_FORMAT
from src.common.Utils import to_datetime, from_datetime


class RosterFileHandler(RaidAndRosterFileHandler):
    def __init__(self):
        super(RosterFileHandler, self).__init__(ROSTER_STORAGE)

    def load(self, raid_name, raid_datetime=None, file_index=None):
        roster = super(RosterFileHandler, self).load(raid_name, raid_datetime, file_index=file_index)
        roster['created_at'] = to_datetime(roster['created_at'], fmt=DATETIMESEC_FORMAT)
        roster['updated_at'] = to_datetime(roster['updated_at'], fmt=DATETIMESEC_FORMAT)
        return roster

    def save(self, roster, file_index=None):
        roster['created_at'] = from_datetime(roster['created_at'], fmt=DATETIMESEC_FORMAT)
        roster['updated_at'] = from_datetime(roster['updated_at'], fmt=DATETIMESEC_FORMAT)
        super(RosterFileHandler, self).save(roster, file_index=file_index)
