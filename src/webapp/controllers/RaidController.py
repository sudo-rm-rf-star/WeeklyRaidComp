from .AbstractController import AbstractController
from datetime import datetime, timedelta
from utils.Constants import abbrev_to_full
from logic.RaidEvent import RaidEvent
from events.raid.RaidEventCreated import RaidEventCreated
import logging


class RaidController(AbstractController):
    def __init__(self, *args, **kwargs):
        super(RaidController, self).__init__(*args, **kwargs)

    def view_directory(self):
        return 'raid'

    def index(self):
        since = datetime.now() - timedelta(weeks=2)
        raids = sorted(self.raids_table.list_raid_events_for_guild(self.guild, since=since.timestamp()),
                       key=lambda event: event.get_datetime())
        return self.view('index', raids=raids)

    def create(self):
        raid_options = list(abbrev_to_full.items())
        team_options = [(raid_group.id, raid_group.name) for raid_group in self.guild.raid_groups]
        return self.view('create', raid_options=raid_options, team_options=team_options)

    def show(self, team_id, name, timestamp):
        dt = datetime.fromtimestamp(timestamp)
        raid = self.raids_table.get_raid_event(self.guild_id, team_id, name, dt)
        return self.view('show', raid=raid, player=self.player)

    def store(self, form):
        logging.getLogger(f'Creating raid event using {form}')
        raid_datetime = datetime.strptime(f"{form['date']} {form['time']}", "%Y-%m-%d %H:%M")
        raid_event = RaidEvent(name=form['name'], raid_datetime=raid_datetime, guild_id=self.guild_id,
                               group_id=form['team_id'])
        self.raids_table.create_raid_event(raid_event)
        self.event_queue.send_event(RaidEventCreated(raid_event))
        return self.redirect('.raid', team_id=raid_event.team_id, name=raid_event.name, timestamp=raid_event.timestamp)

    def signup_remind(self, name, timestamp):
        return self.redirect('.raid', team_id=None, name=name, timestamp=timestamp)

    def create_roster(self, name, timestamp):
        return self.redirect('.raid', team_id=None, name=name, timestamp=timestamp)
