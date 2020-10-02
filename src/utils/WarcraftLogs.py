import requests
import re
import os
from dotenv import load_dotenv
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from typing import Dict, List
from datetime import datetime, timedelta
from collections import defaultdict
from utils.DateOptionalTime import DateOptionalTime
from utils.Date import Date
from typing import Optional
from utils.Constants import abbrev_raid_name
from logic.Report import Fight, Report
from logic.RaidEvent import RaidEvent
from utils.Consumables import get_consumable_requirements
from client.RaidEventsResource import RaidEventsResource
import utils.Logger as Log
from exceptions.InvalidArgumentException import InvalidArgumentException


def attendance_query(guild_id: int, page: int) -> str:
    return """
    query { 
      guildData { 
        guild(id: """ + str(guild_id) + """) {
          attendance(page: """ + str(page) + """) {
            current_page
            last_page
            data {
              code
              zone {
                name
              }
              startTime
              players {
                presence
                name
              }
            }
          }
        }
      }
    }
    """


def report_fights_query(report_id: str) -> str:
    return """
    query { 
      reportData { 
        report(code: """ + f'"{report_id}"' + """) {
          masterData { 
            actors(type: "Player") { 
                id
                name
            }
            abilities {
                name
                gameID
            }
          }
          fights {
              bossPercentage
              name
              startTime
              endTime
              friendlyPlayers
          }
        }
      }
    }
    """


def report_casts_or_buffs_query(report_id: str, start_time: int, end_time: int, abilityId: int,
                                casts_or_buffs: str) -> str:
    return """
    query { 
      reportData { 
        report(code: """ + f'"{report_id}"' + """) {
            events(""" + f'startTime: {start_time}, endTime: {end_time}, dataType: {casts_or_buffs}, abilityID: {abilityId}' + """) {
                nextPageTimestamp
                data
            }
        }
      }
    }
    """


BASE = 'https://www.warcraftlogs.com/api/v2/client'
TOKEN_URL = f'https://www.warcraftlogs.com/oauth/token'
BEARER_TOKEN = None


class WarcraftLogs:
    def __init__(self, events_resource: RaidEventsResource, guild_id: int):
        if guild_id is None:
            raise InvalidArgumentException(f'This function is not usable without Warcraft Logs. '
                                           f'Make sure your guild name, realm and region matches your guild in '
                                           f'Warcraft Logs. You can update this info by using `!guild edit`')

        self.auth_header = {}
        self.expiry_datetime = datetime.now()
        self.guild_id = guild_id
        self.events_resource = events_resource

    def get_auth_header(self) -> Dict[str, str]:
        if datetime.now() >= self.expiry_datetime:
            load_dotenv()
            client_id = os.getenv('WL_CLIENT_ID')
            client_secret = os.getenv('WL_CLIENT_SECRET')
            client = BackendApplicationClient(client_id=client_id)
            oauth = OAuth2Session(client=client)
            token = dict(oauth.fetch_token(token_url=TOKEN_URL, client_id=client_id, client_secret=client_secret))
            print(token['access_token'])
            exit(1)
            self.expiry_datetime = datetime.now() + timedelta(seconds=int(token['expires_in']))
            self.auth_header = {"Content-Type": "application/json",
                                "Authorization": f"{token['token_type']} {token['access_token']}"}
        return self.auth_header

    def get_attendance(self, raid_events: List[RaidEvent]) -> Dict[str, Dict[str, List[datetime]]]:
        """ Gets the present dates per player per raid in the given list """
        attendance = defaultdict(lambda: defaultdict(set))
        self.sync_raids(raid_events)
        for raid_event in raid_events:
            for player in raid_event.presence:
                attendance[player][raid_event.name].add(raid_event.get_datetime())
        return {k: dict(v) for k, v in attendance.items()}

    def get_report(self, raid_event: RaidEvent):
        self.sync_raids([raid_event])
        report_code = raid_event.report_code
        report = self.make_request(report_fights_query(report_code))['data']['reportData']['report']
        actors = {actor['id']: actor['name'] for actor in report['masterData']['actors']}
        fights = []
        for fight in report['fights']:
            boss_percentage = fight.get('bossPercentage')
            if fight.get('friendlyPlayers'):
                fights.append(Fight(fight['name'], fight['startTime'] // 1000, fight['endTime'] // 1000,
                                    present_players={actors[actor] for actor in fight['friendlyPlayers']},
                                    boss_percentage=boss_percentage))

        buff_counts = defaultdict(lambda: defaultdict(int))
        abilities = [(ability['name'].strip(), ability['gameID']) for ability in report['masterData']['abilities']]
        for consumable_requirement in get_consumable_requirements(raid_event.name):
            consumables = consumable_requirement.consumable_names
            consumable_ids = [ability_id for ability_name, ability_id in abilities if
                              ability_name in consumables]  # One consumable name can map onto multiple ids...
            if len(consumable_ids) == 0:
                Log.warn(f'Could not find {consumables}')
            for consumable_id in consumable_ids:
                events = self.get_events(report_code, 0, fights[-1].end_time * 1000, consumable_id)
                for event in events:
                    source_id = event['sourceID']
                    target_id = event['targetID']
                    player = actors.get(source_id, actors.get(target_id))
                    if player:
                        buff_counts[tuple(consumables)][player] += 1
        return Report(code=report_code, fights=fights, buff_counts=dict(buff_counts))

    def get_events(self, report_code: str, start_time: int, end_time: int, consumable_id: int):
        buffs = [buff for buff in self._get_events(report_code, start_time, end_time, consumable_id, "Buffs") if
                 buff['type'] == 'applybuff']
        # casts = self._get_events(report_code, start_time, end_time, consumable_id, "Casts")
        casts = []
        return buffs + casts

    def _get_events(self, report_code: str, start_time: int, end_time: int, consumable_id: int, casts_or_buffs: str):
        events = []
        while start_time is not None:
            response = self.make_request(
                report_casts_or_buffs_query(report_code, start_time, end_time, consumable_id,
                                            casts_or_buffs=casts_or_buffs))['data']['reportData']['report']['events']
            start_time = response.get('nextPageTimestamp', None)
            events.extend(response['data'])
        return events

    def sync_raids(self, raid_events: Optional[List[RaidEvent]] = None):
        """ Scans all the raids from warcraft logs for the given events. Scans everything if raid_events is None """
        current_page = 1
        last_page = None
        updated_raids = []

        while (last_page is None or current_page < last_page) and any(
                not raid_event.has_been_scanned for raid_event in raid_events):
            result = self.make_attendance_request(current_page)
            last_page = result['last_page']
            for raid in result['data']:
                raid_name = abbrev_raid_name[raid['zone']['name']]
                raid_date = DateOptionalTime.from_date(datetime.fromtimestamp(raid['startTime'] / 1000))
                raid_event = _find_raid(raid_name, raid_date, raid_events)
                if raid_event:
                    raid_event.report_code = raid['code']
                    raid_event.presence = [player['name'] for player in raid['players'] if player['presence'] == 1]
                    raid_event.has_been_scanned = True
                    updated_raids.append(raid_event)
            current_page += 1

        # If any event was not found, we do not have to try anymore in the future.
        for raid_event in raid_events:
            if not raid_event.has_been_scanned:
                raid_event.has_been_scanned = True
                raid_event.presence = []
                updated_raids.append(raid_event)

        for raid_event in updated_raids:
            self.events_resource.update_raid_raw(raid_event)

    def make_attendance_request(self, page):
        query = attendance_query(self.guild_id, page)
        return self.make_request(query)['data']['guildData']['guild']['attendance']

    def make_request(self, query: str):
        response = requests.post(BASE, json={'query': query}, headers=self.get_auth_header())
        try:
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    "Query failed to run by returning code of {}: {}. {}".format(response.status_code, response.text,
                                                                                 query))
        except KeyError as ex:
            Log.error(f"Response to query is malformed: {response.json()}")
            raise ex


def _find_raid(raid_name: str, raid_date: Date, raid_events: List[RaidEvent]) -> Optional[RaidEvent]:
    for raid_event in raid_events:
        if raid_event.name == raid_name and raid_event.datetime == raid_date:
            return raid_event
    return None


def get_wl_guild_id(guild: str, region: str, realm: str) -> Optional[str]:
    url = f'https://classic.warcraftlogs.com/guild/{region}/{realm}/{guild}'
    response = requests.get(url)
    wl_guild_ids = re.findall(r'/guild/id/([0-9]*)', response.text)
    wl_guild_id = wl_guild_ids[0] if len(wl_guild_ids) >= 1 else None
    return wl_guild_id


def get_raidgroups(wl_guild_id: int) -> Optional[Dict[str, int]]:
    if wl_guild_id is None:
        return None
    url = f'https://classic.warcraftlogs.com/guild/id/{wl_guild_id}'
    response = requests.get(url)
    raid_groups = re.findall(r'/guild/team-calendar/([0-9]*)">([^<]*)', response.text)
    if len(raid_groups) == 0:
        return None
    return {v: int(k) for k, v in raid_groups}


if __name__ == '__main__':
    wl_guild_id = 510080
    print(get_raidgroups(wl_guild_id))
