import requests
import os
from dotenv import load_dotenv
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from typing import Dict, List
from datetime import datetime, timedelta
from collections import defaultdict
import utils.Logger as Log
from utils.Date import Date
from typing import Optional
from datetime import date
from utils.Constants import abbrev_raid_name
from logic.Report import Fight, Report


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


def report_query(report_id: str) -> str:
    return """
    query { 
      reportData { 
        report(code: """ + f'"{report_id}"' + """) {
          masterData { 
            actors(type: "Player") { 
            id
            name
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
            self.auth_header = {"Content-Type": "application/json", "Authorization": f"{token['token_type']} {token['access_token']}"}
        return self.auth_header

    def get_attendance(self) -> Dict[str, Dict[str, List[datetime]]]:
        """Gets the present dates per player per raid"""
        attendance = defaultdict(lambda: defaultdict(set))
        for (raid_name, raid_date, present_players, _) in self.get_raids():
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
        report = self.make_request(report_query(report_code))['data']['reportData']['report']
        actors = {actor['id']: actor['name'] for actor in report['masterData']['actors']}
        fights = []
        for fight in self.make_request(report_query(report_code))['data']['reportData']['report']['fights']:
            if fight['bossPercentage'] == 0:
                fights.append(Fight(fight['name'], fight['startTime'] // 1000, fight['endTime'] // 1000, {actors[actor] for actor in fight['friendlyPlayers']}))
        return Report(code=report_code, fights=fights)

    def get_raids(self):
        """ Possible bottleneck """
        raids = []
        current_page = 1
        last_page = None
        while last_page is None or current_page < last_page:
            result = self.make_attendance_request(current_page)
            last_page = result['last_page']
            for raid in result['data']:
                yield (  # raid_name, raid_datetime, present_players, report_code
                    abbrev_raid_name[raid['zone']['name']],
                    Date(datetime.fromtimestamp(raid['startTime'] / 1000).date()),
                    [player['name'] for player in raid['players'] if player['presence'] == 1],
                    raid['code']
                )
            raids.extend(result['data'])
            current_page += 1
        return raids

    def make_attendance_request(self, page):
        query = attendance_query(self.guild_id, page)
        return self.make_request(query)['data']['guildData']['guild']['attendance']

    def make_request(self, query: str):
        response = requests.post(BASE, json={'query': query}, headers=self.get_auth_header())
        try:
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception("Query failed to run by returning code of {}: {}. {}".format(response.status_code, response.text, query))
        except KeyError as ex:
            Log.error(f"Response to query is malformed: {response.json()}")
            raise ex

