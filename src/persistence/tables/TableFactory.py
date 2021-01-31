from utils.Singleton import Singleton
from persistence.tables.PlayersTable import PlayersTable
from persistence.tables.RaidEventsTable import RaidEventsTable
from persistence.tables.GuildsTable import GuildsTable
import boto3
from dotenv import load_dotenv
import os
from persistence.tables.MessagesTable import MessagesTable


class TableFactory(metaclass=Singleton):
    def __init__(self):
        load_dotenv()
        access_key = os.getenv('AWS_ACCESS_KEY')
        secret_key = os.getenv('AWS_SECRET_KEY')
        self.ddb = boto3.resource('dynamodb', region_name='eu-west-1', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    def get_players_table(self) -> PlayersTable:
        return PlayersTable(self.ddb)

    def get_raid_events_table(self) -> RaidEventsTable:
        return RaidEventsTable(self.ddb)

    def get_guilds_table(self) -> GuildsTable:
        return GuildsTable(self.ddb)

    def get_messages_table(self) -> MessagesTable:
        return MessagesTable(self.ddb)
