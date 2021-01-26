from .AbstractController import AbstractController
from utils.DateOptionalTime import DateOptionalTime
from datetime import datetime, timedelta
from utils.Constants import abbrev_to_full
from logic.RaidEvent import RaidEvent
from logic.MessageRef import MessageRef
import discord


class RaidController(AbstractController):
    def __init__(self, *args, **kwargs):
        super(RaidController, self).__init__(*args, **kwargs)

    def view_directory(self):
        return 'raid'

    def index(self):
        since = datetime.now() - timedelta(weeks=2)
        raids = sorted(self.events_table.list_raid_events(self.guild_id, self.group_id, since=since.timestamp()),
                       key=lambda event: event.get_datetime())
        return self.view('index', raids=raids)

    def create(self):
        return self.view('create', options=list(abbrev_to_full.items()))

    def show(self, name, timestamp):
        dt = DateOptionalTime.from_timestamp(timestamp)
        raid = self.events_table.get_raid_event(self.guild_id, self.group_id, name, dt)
        return self.view('show', raid=raid)

    def store(self, form):
        raid_datetime = datetime.strptime(f"{form['date']} {form['time']}", "%Y-%m-%d %H:%M")
        raid_event = RaidEvent(name=form['name'], raid_datetime=raid_datetime, guild_id=self.guild_id,
                               group_id=self.group_id)
        return self.redirect('.raid', name='', timestamp=0)

    def signup_remind(self, name, timestamp):
        return self.redirect('.raid', name=name, timestamp=timestamp)

    def create_roster(self, name, timestamp):
        return self.redirect('.raid', name=name, timestamp=timestamp)
