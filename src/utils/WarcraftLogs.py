import requests
import os
from dotenv import load_dotenv
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from typing import Dict, List
from datetime import datetime, timedelta
from utils.Constants import raid_abbrev_long
from collections import defaultdict
import utils.Logger as Log
from utils.DateOptionalTime import DateOptionalTime
from utils.Date import Date


def attendance_query(guild_id: int, page: int) -> str:
    return """
    query { 
      guildData { 
        guild(id: """ + str(guild_id) + """) {
          attendance(page: """ + str(page) + """) {
            current_page
            last_page
            data {
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
        current_page = 1
        last_page = None
        while last_page is None or current_page < last_page:
            result = self.make_attendance_request(current_page)
            last_page = result['last_page']
            for raid in result['data']:
                raid_name = raid_abbrev_long[raid['zone']['name']]
                raid_date = Date(datetime.fromtimestamp(raid['startTime']/1000).date())
                present_players = [player['name'] for player in raid['players'] if player['presence'] == 1]
                for player in present_players:
                    attendance[player][raid_name].add(raid_date)
            current_page += 1
        return {k: dict(v) for k, v in attendance.items()}

    def make_attendance_request(self, page):
        query = attendance_query(self.guild_id, page)
        response = requests.post(BASE, json={'query': query}, headers=self.get_auth_header())
        try:
            if response.status_code == 200:
                return response.json()['data']['guildData']['guild']['attendance']
            else:
                raise Exception("Query failed to run by returning code of {}: {}. {}".format(response.status_code, response.text, query))
        except KeyError as ex:
            Log.error(f"Response to query is malformed: {response.json()}")
            raise ex


if __name__ == '__main__':
    attendance = WarcraftLogs(510080).get_attendance()
    print(attendance['Dok'])
