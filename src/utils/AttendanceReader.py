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
from utils.WarcraftLogs import WarcraftLogs


def update_raid_presence(guild_id: int, group_id: int, wl_guild_id: int, events_resource: RaidEventsResource, players_resource: PlayersResource) -> None:
    players = players_resource.list_players(guild_id)
    raid_events = events_resource.get_raids(guild_id, group_id)
    attendance = WarcraftLogs(wl_guild_id).get_attendance()
    for raid_event in raid_events:
        raid_name = raid_event.get_name(abbrev=True)
        raid_datetime = raid_event.get_datetime()
        for player in players:
            was_present = False
            was_standby = False
            for character in player.characters:
                if raid_datetime.date in attendance.get(character.name, {}).get(raid_name, {}):
                    was_present = True
                elif raid_event.has_char_signed(character):
                    was_standby = True
            if was_present:
                player.add_present_date(raid_name, raid_datetime)
            elif was_standby:
                player.add_standby_date(raid_name, raid_datetime)

    for player in players:
        players_resource.update_player(player)
