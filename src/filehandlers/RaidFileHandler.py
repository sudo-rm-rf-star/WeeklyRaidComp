from src.common.Constants import RAID_STORAGE
import pickle
from typing import List
from src.logic.RaidEvent import RaidEvent


def load_raid_events() -> List[RaidEvent]:
    """ Loading all the data is not great in a high volume space but we only need to load it in-memory once so performance should be okay.
    If storage is ever a problem, we need to move to a proper database. """
    try:
        with open(RAID_STORAGE, mode='rb') as raid_events_file:
            return pickle.load(raid_events_file)
    except FileNotFoundError:
        return []


def save_raid_events(raid_events: List[RaidEvent]) -> None:
    with open(RAID_STORAGE, mode='wb+') as raid_events_file:
        pickle.dump(raid_events, raid_events_file)
