from src.filehandlers.RaidAndRosterFileHandler import RaidAndRosterFileHandler
from src.common.Constants import ROSTER_STORAGE
from src.common.Utils import to_datetime, from_datetime


class RosterFileHandler(RaidAndRosterFileHandler):
    def __init__(self):
        super(RosterFileHandler, self).__init__(ROSTER_STORAGE)

    def load(self, raid_name, raid_datetime=None):
        roster = super(RosterFileHandler, self).load(raid_name, raid_datetime)
        roster['created_at'] = to_datetime(roster['created_at'])
        roster['updated_at'] = to_datetime(roster['updated_at'])
        return roster

    def save(self, roster):
        roster['created_at'] = from_datetime(roster['created_at'])
        roster['updated_at'] = from_datetime(roster['updated_at'])
        super(RosterFileHandler, self).save(roster)
