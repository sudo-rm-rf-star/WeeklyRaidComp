from persistence.tables.TableFactory import TableFactory
from flask_discord import DiscordOAuth2Session
from .RaidController import RaidController
from .HomeController import HomeController
from .PlayerController import PlayerController
from .GuildController import GuildController
from events.EventQueue import EventQueue


class ControllerFactory:
    def __init__(self, session: DiscordOAuth2Session):
        self.session = session
        self.user = session.fetch_user()
        table_factory = TableFactory()
        self.player = table_factory.get_players_table().get_player_by_id(self.user.id)
        self.raidteam = table_factory.get_raid_teams_table().get_raidteam(self.player.selected_guild_id,
                                                                          self.player.selected_team_name)

    def create_raid_controller(self):
        return RaidController(**self._abstract_controller_kwargs())

    def create_home_controller(self):
        return HomeController(**self._abstract_controller_kwargs())

    def create_player_controller(self):
        return PlayerController(**self._abstract_controller_kwargs())

    def create_guild_controller(self):
        return GuildController(**self._abstract_controller_kwargs())

    def _abstract_controller_kwargs(self):
        return {
            "session": self.session,
            "user": self.user,
            "player": self.player,
            "raidteam": self.raidteam
        }
