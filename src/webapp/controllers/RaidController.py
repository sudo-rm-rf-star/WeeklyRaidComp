from .AbstractController import AbstractController
from datetime import datetime
from utils.Constants import full_raid_names
from exceptions.InvalidInputException import InvalidInputException
import logging
from persistence.RaidEventsResource import RaidEventsResource


class RaidController(AbstractController):
    def __init__(self, *args, **kwargs):
        super(RaidController, self).__init__(*args, **kwargs)
        self.raids_resource = RaidEventsResource()

    def view_directory(self):
        return 'raid'

    def index(self):
        since = datetime.now()
        raids = sorted(self.raids_table.list_raid_events_for_guild(self.guild, since=since.timestamp()),
                       key=lambda event: event.get_datetime())
        return self.view('index', raids=raids)

    def create(self, errors=None):
        raid_options = list(full_raid_names.items())
        team_options = [(raid_group.id, raid_group.name) for raid_group in self.guild.raid_groups]
        return self.view('create', raid_options=raid_options, team_options=team_options, errors=errors)

    def show(self, team_id, name, timestamp):
        dt = datetime.fromtimestamp(timestamp)
        raid = self.raids_table.get_raid(self.guild_id, team_id, name, dt)
        return self.view('show', raid=raid, player=self.player)

    def store(self, form):
        logging.getLogger(f'Creating raid event using {form}')
        raid_event, errors = self.verify_form_and_create_raid(form)
        if len(errors) > 0:
            return self.create(errors)
        else:
            return self.redirect('.raid', team_id=raid_event.team_id, name=raid_event.name,
                                 timestamp=raid_event.timestamp)

    def send_reminder(self, team_id, name, timestamp):
        return self.redirect('.raid', team_id=team_id, name=name, timestamp=timestamp)

    def create_roster(self, team_id, name, timestamp):
        return self.redirect('.raid', team_id=team_id, name=name, timestamp=timestamp)

    def invite_player(self, team_id, name, timestamp):
        return self.redirect('.raid', team_id=team_id, name=name, timestamp=timestamp)

    def verify_form_and_create_raid(self, form):
        errors = []
        form_date = form.get('date')
        form_time = form.get('time')
        form_name = form.get('name')
        form_team_id = form.get('team_id')
        raid_event = None
        if not form_date:
            errors.append('Date must be set.')
        if not form_time:
            errors.append('Time must be set.')
        if not form_team_id:
            errors.append('Team must be set')
        if not form_name:
            errors.append('Raid name must be set')
        if form_date and form_time:
            raid_datetime = datetime.strptime(f"{form_date} {form_time}", "%Y-%m-%d %H:%M")
            if raid_datetime < datetime.now():
                errors.append('Raid must be in future')
            else:
                if form_name and form_team_id:
                    try:
                        raid_event = self.raids_resource.create_raid(raid_name=form['name'], raid_datetime=raid_datetime,
                                                                     guild_id=self.guild_id, group_id=form['team_id'])
                    except InvalidInputException as e:
                        errors.append(e.message)
        return raid_event, errors
