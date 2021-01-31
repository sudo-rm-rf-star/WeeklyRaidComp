from .EventHandler import EventHandler
from .Event import Event
from pydoc import locate
from exceptions.InternalBotException import InternalBotException
from persistence.tables.MessagesTable import MessagesTable
from persistence.tables.RaidEventsTable import RaidEventsTable
from persistence.tables.GuildsTable import GuildsTable
from persistence.tables.PlayersTable import PlayersTable


class EventHandlerFactory:
    def __init__(self, discord_client, raids_table: RaidEventsTable, guilds_table: GuildsTable,
                 players_table: PlayersTable, messages_table: MessagesTable):
        self.discord_client = discord_client
        self.raids_table = raids_table
        self.guilds_table = guilds_table
        self.players_table = players_table
        self.messages_table = messages_table

    def create_event_handler(self, event: Event) -> EventHandler:
        event_name = type(event).__name__
        name = fullname(event).replace(event_name, event_name + "Handler")
        try:
            return locate(name)(discord_client=self.discord_client, raids_table=self.raids_table,
                                guilds_table=self.guilds_table, players_table=self.players_table,
                                messages_table=self.messages_table)
        except TypeError as e:
            raise InternalBotException(f"Could not initialize handler {name} for {type(event)} because of {e}")


def fullname(o):
    # o.__module__ + "." + o.__class__.__qualname__ is an example in
    # this context of H.L. Mencken's "neat, plausible, and wrong."
    # Python makes no guarantees as to whether the __module__ special
    # attribute is defined, so we take a more circumspect approach.
    # Alas, the module name is explicitly excluded from __qualname__
    # in Python 3.

    module = o.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return o.__class__.__name__  # Avoid reporting __builtin__
    else:
        return module + '.' + o.__class__.__name__
