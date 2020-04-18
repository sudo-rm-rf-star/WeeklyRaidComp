from src.filehandlers.RaidAndRosterFileHandler import RaidAndRosterFileHandler
from src.common.Constants import RAID_STORAGE


class RaidFileHandler(RaidAndRosterFileHandler):
    def __init__(self):
        super(RaidFileHandler, self).__init__(RAID_STORAGE)

