import re
from datetime import datetime, timedelta
from typing import List, Any

import requests

from client.PlayersResource import PlayersResource
from client.RaidEventsResource import RaidEventsResource
from exceptions.InvalidArgumentException import InvalidArgumentException
from utils.Constants import USE_SIGNUP_HISTORY, WARCRAFT_LOGS_TEAM_ID, WARCRAFT_LOGS_GUILD_ID, ZONE_ID, SUPPORTED_RAIDS
from utils.Date import Date
from utils.DateOptionalTime import DateOptionalTime


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
last_updated_at = None


def update_raid_presence(players_resource: PlayersResource, events_resource: RaidEventsResource) -> None:
    """ Currently there is a lot of overhead every timeutil this method is called as everything is recomputed. The current way of querying WL logs doesn't
    allow a more efficient way of handling this. We only do this operation at most once a day or upon startup. """
    return  # TODO
    global last_updated_at
    if last_updated_at is None or last_updated_at + timedelta(days=1) < datetime.now():
        last_updated_at = datetime.now()
    else:
        return

    raid_events = events_resource.get_raids()
    players = {player.name: player for player in players_resource.list_players()}
    updated_players = set()
    for raid_name in SUPPORTED_RAIDS:
        for raid_attendance_html in get_raid_attendance_htmls(raid_name):
            dates = list(map(lambda x: DateOptionalTime(Date(datetime.fromtimestamp(float(x) / 1000).date())), re.findall(hdr_rex, raid_attendance_html)))
            charnames = re.findall(row_rex, raid_attendance_html)
            was_present = list(map(lambda x: x == 'present', re.findall(col_rex, raid_attendance_html)))
            for player_name, presence in zip(charnames, chunks(was_present, len(dates))):
                if player_name in players:
                    player = players[player_name]
                    player_computed_dates = player.get_standby_dates(raid_name).union(player.get_present_dates(raid_name))
                    for date, present in zip(dates, presence):
                        if date not in player_computed_dates:
                            try:
                                raid = next(raid_event for raid_event in raid_events if raid_event.name == raid_name and raid_event.get_datetime() == date)
                                if present:
                                    player.add_present_date(raid.name, raid.datetime)
                                # A character counts for standby if he signed up for the raid and he was not present in the raid.
                                elif not USE_SIGNUP_HISTORY or player_name in raid.roster.signee_choices:
                                    player.add_standby_date(raid.name, raid.datetime)
                                updated_players.add(player)
                            except StopIteration:
                                pass
    for player in updated_players:
        players_resource.update_player(player)


def chunks(lst: List[Any], n: int) -> List[List[Any]]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
