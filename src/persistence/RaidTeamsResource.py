from utils.Singleton import Singleton
from .tables.TableFactory import TableFactory
from events.EventQueue import EventQueue
from logic.RaidTeam import RaidTeam
from exceptions.InvalidInputException import InvalidInputException
from typing import Optional, List


class RaidTeamsResource(metaclass=Singleton):
    def __init__(self):
        self.table = TableFactory().get_raid_teams_table()
        self.queue = EventQueue()

    def create_raidteam(self, raidteam: RaidTeam):
        if self.get_raidteam(team_name=raidteam.name, guild_id=raidteam.guild_id) is not None:
            raise InvalidInputException(f'A team with the same name already exists.')
        self.table.create_raidteam(raidteam)

    def get_raidteam(self, guild_id: int, team_name: str) -> Optional[RaidTeam]:
        return self.table.get_raidteam(team_name=team_name, guild_id=guild_id)

    def list_raidteams(self, guild_id: int) -> List[RaidTeam]:
        return self.table.list_raidteams(guild_id=guild_id)

