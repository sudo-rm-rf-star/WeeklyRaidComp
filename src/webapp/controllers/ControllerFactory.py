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
        self.event_queue = EventQueue()
        table_factory = TableFactory()
        self.players_table = table_factory.get_players_table()
        self.guilds_table = table_factory.get_guilds_table()
        self.messages_table = table_factory.get_messages_table()
        self.raids_table = table_factory.get_raid_events_table()
        self.player = self.players_table.get_player_by_id(self.user.id)
        self.guild = None
        if self.player:
            self.guild = self.guilds_table.get_guild(self.player.selected_guild_id) if self.player else None

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
            "player": self.player,
            "guild": self.guild,
            "raids_table": self.raids_table,
            "players_table": self.players_table,
            "guilds_table": self.guilds_table,
            "event_queue": self.event_queue
        }
