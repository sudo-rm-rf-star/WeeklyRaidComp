from .AbstractController import AbstractController
from utils.DateOptionalTime import DateOptionalTime


class RaidController(AbstractController):
    def __init__(self, *args, **kwargs):
        super(RaidController, self).__init__(*args, **kwargs)

    def view_directory(self):
        return 'raid'

    def index(self):
        raids = sorted(self.events_table.list_raid_events(self.guild_id, self.group_id),
                       key=lambda event: event.get_datetime(), reverse=True)
        return self.view('index', raids=raids)

    def create(self):
        return self.view('create')

    def show(self, name, timestamp):
        dt = DateOptionalTime.from_timestamp(timestamp)
        raid = self.events_table.get_raid_event(self.guild_id, self.group_id, name, dt)
        return self.view('show', raid=raid)

    def store(self, form):
        return self.redirect('raid', name='', timestamp=0)

    def signup_remind(self, name, timestamp):
        return self.redirect('raid', name=name, timestamp=timestamp)

    def create_roster(self, name, timestamp):
        return self.redirect('raid', name=name, timestamp=timestamp)
