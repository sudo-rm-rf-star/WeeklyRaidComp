import requests
import os
from dotenv import load_dotenv
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from typing import Dict, List
from datetime import datetime, timedelta
from collections import defaultdict
from utils.Date import Date
from typing import Optional
from utils.Constants import abbrev_raid_name
from logic.Report import Fight, Report
from utils.Consumables import get_consumable_requirements
import utils.Logger as Log


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
    def __init__(self, guild_id):
        self.auth_header = {}
        self.expiry_datetime = datetime.now()
        self.guild_id = guild_id

    def get_auth_header(self) -> Dict[str, str]:
        if datetime.now() >= self.expiry_datetime:
            load_dotenv()
            client_id = os.getenv('WL_CLIENT_ID')
            client_secret = os.getenv('WL_CLIENT_SECRET')
            client = BackendApplicationClient(client_id=client_id)
            oauth = OAuth2Session(client=client)
            token = dict(oauth.fetch_token(token_url=TOKEN_URL, client_id=client_id, client_secret=client_secret))
            self.expiry_datetime = datetime.now() + timedelta(seconds=int(token['expires_in']))
            self.auth_header = {"Content-Type": "application/json",
                                "Authorization": f"{token['token_type']} {token['access_token']}"}
        return self.auth_header

    def get_attendance(self, do_not_scan_before: datetime) -> Dict[str, Dict[str, List[datetime]]]:
        """Gets the present dates per player per raid"""
        attendance = defaultdict(lambda: defaultdict(set))
        raids = self.get_raids(do_not_scan_before)
        print(len(list(raids)))
        for (raid_name, raid_date, present_players, _) in raids:
            for player in present_players:
                attendance[player][raid_name].add(raid_date)
        return {k: dict(v) for k, v in attendance.items()}

    def get_report_code(self, raid_name, raid_date) -> Optional[str]:
        """Gets the report codes for every raid"""
        for (raid_name2, raid_date2, _, report_code) in self.get_raids():
            if raid_name == raid_name2 and raid_date == raid_date2:  # Naming is difficult okay...
                return report_code

    def get_report(self, raid_name, raid_date):
        report_code = self.get_report_code(raid_name, raid_date)
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
        for consumable_requirement in get_consumable_requirements(raid_name):
            consumables = consumable_requirement.consumable_names
            abilities = [(ability['name'].strip(), ability['gameID']) for ability in report['masterData']['abilities']]

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
        buffs = self._get_events(report_code, start_time, end_time, consumable_id, "Buffs")
        casts = self._get_events(report_code, start_time, end_time, consumable_id, "Casts")
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

    def get_raids(self, do_not_scan_before: Optional[datetime] = None):
        """ Possible bottleneck """
        current_page = 1
        last_page = None
        scanned_until = datetime.now()
        '''
        We stop scanning if
        1) We have reached the last page
        2) We have reached a page we have already scanned
        3) We have scanned for more than 20 seconds
        '''
        scan_start = datetime.now().second
        scan_time = 0
        while (last_page is None or current_page < last_page) and (
                do_not_scan_before is None or do_not_scan_before < scanned_until)\
                and scan_time <= 20:
            result = self.make_attendance_request(current_page)
            last_page = result['last_page']
            for raid in result['data']:
                scanned_until = datetime.fromtimestamp(raid['startTime'] / 1000)
                yield (  # raid_name, raid_datetime, present_players, report_code
                    abbrev_raid_name[raid['zone']['name']],
                    Date(scanned_until.date()),
                    [player['name'] for player in raid['players'] if player['presence'] == 1],
                    raid['code']
                )
            scan_time = datetime.now().second - scan_start
            current_page += 1

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
