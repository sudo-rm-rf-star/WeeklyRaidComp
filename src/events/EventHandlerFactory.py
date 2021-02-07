from .EventHandler import EventHandler
from .Event import Event
from pydoc import locate
from exceptions.InternalBotException import InternalBotException


class EventHandlerFactory:
    def __init__(self, discord_client):
        self.discord_client = discord_client

    def create_event_handler(self, event: Event) -> EventHandler:
        event_name = type(event).__name__
        name = fullname(event).replace(event_name, event_name + "Handler")
        try:
            return locate(name)(discord_client=self.discord_client)
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
