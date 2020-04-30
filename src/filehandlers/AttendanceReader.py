import re
import requests
from src.time.DateOptionalTime import DateOptionalTime
from src.logic.RaidEvents import RaidEvents
from src.logic.Players import Players
from src.common.Constants import USE_SIGNUP_HISTORY, WARCRAFT_LOGS_TEAM_ID, WARCRAFT_LOGS_GUILD_ID, ZONE_ID, SUPPORTED_RAIDS
from src.exceptions.InvalidArgumentException import InvalidArgumentException
from datetime import datetime
from typing import List, Any


# https://classic.warcraftlogs.com/guild/attendance/510080
def get_raid_attendance_htmls(raid_name: str, guild_id: str = WARCRAFT_LOGS_GUILD_ID, team_id: str = WARCRAFT_LOGS_TEAM_ID) -> List[str]:
    if not guild_id:
        raise InvalidArgumentException(f'A guild id must be specified for fetching Warcraft Logs history')
    if raid_name and raid_name not in ZONE_ID:
        raise InvalidArgumentException(f'{raid_name} is not yet supported')
    zone_id = ZONE_ID[raid_name]
    wl_url = f'https://classic.warcraftlogs.com/guild/attendance-table/{guild_id}/{team_id}/{zone_id}'
    content = requests.get(wl_url).text
    htmls = [content]
    urls = re.findall(wl_url, content)
    for url in urls:
        htmls.append(requests.get(url).text)
    return htmls


hdr_rex = r'var createdDate = new Date\(([0-9]*)\)'
row_rex = r'<tr><td[^>]*>([a-zA-ZöÓòéëû]*)'
col_rex = '(present|absent)'


def update_raid_presence() -> None:
    """ Currently there is a lot of overhead every time this method is called as everything is recomputed. The current way of querying WL logs doesn't
    allow a more efficient way of handling this """
    for raid_name in SUPPORTED_RAIDS:
        for raid_attendance_html in get_raid_attendance_htmls(raid_name):
            dates = list(map(lambda x: DateOptionalTime(datetime.fromtimestamp(float(x) / 1000).date()), re.findall(hdr_rex, raid_attendance_html)))
            charnames = re.findall(row_rex, raid_attendance_html)
            was_present = list(map(lambda x: x == 'present', re.findall(col_rex, raid_attendance_html)))
            for player_name, presence in zip(charnames, chunks(was_present, len(dates))):
                player = Players().get(player_name)
                for date, present in zip(dates, presence):
                    raid = RaidEvents().get(date)
                    if present:
                        raid.presence.add(player_name)
                        player.add_present_date(raid.name, raid.datetime)
                    # A character counts for standby if he signed up for the raid and he was not present in the raid.
                    elif not USE_SIGNUP_HISTORY or player_name in raid.signee_choices:
                        player.add_standby_date(raid.name, raid.datetime)
    RaidEvents().store()
    Players().store()


def chunks(lst: List[Any], n: int) -> List[List[Any]]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
