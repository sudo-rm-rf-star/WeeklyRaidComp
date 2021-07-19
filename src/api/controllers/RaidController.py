import json
from flask import render_template, redirect, url_for

from logic.RaidEvent import RaidEvent
from datetime import datetime
from logic.Raid import Raid
from exceptions.InvalidInputException import InvalidInputException
import logging
from persistence.RaidEventsResource import RaidEventsResource


class RaidController:
    def __init__(self, *args, **kwargs):
        super(RaidController, self).__init__(*args, **kwargs)
        self.raids_resource = RaidEventsResource()

    def index(self, guild_id, team_name):
        print(guild_id, team_name)
        return {'data': [raid.to_dict() for raid in
                         sorted(self.raids_resource.list_raids_within_days(guild_id=guild_id, team_name=team_name, days=90),
                                key=lambda event: event.get_datetime())]}

    def get(self, guild_id, team_name, raid_name, raid_datetime):
        return {'data': self.raids_resource.get_raid(raid_name=raid_name, raid_datetime=raid_datetime,
                                                     guild_id=guild_id, team_name=team_name).to_dict()}

    def update(self, data):
        logging.getLogger(f'Creating raid event using {data}')
        raid_event = RaidEvent.from_dict(data)
        self.raids_resource.update_raid(raid_event)
        return {'data': raid_event.to_dict()}

    def store(self, guild_id, team_name, form):
        form['guild_id'] = guild_id
        form['team_name'] = team_name
        logging.getLogger(f'Creating raid event using {form}')
        raid_event, errors = self.verify_form_and_create_raid(form)
        if len(errors) > 0:
            return {'errors': errors}
        else:
            return {'data': raid_event.to_dict()}

    def verify_form_and_create_raid(self, form):
        errors = []
        form_date = form.get('date')
        form_time = form.get('time')
        form_name = form.get('name')
        raid_event = None
        if not form_date:
            errors.append('Date must be set.')
        if not form_time:
            errors.append('Time must be set.')
        if not form_name:
            errors.append('Raid name must be set')
        if form_date and form_time:
            raid_datetime = datetime.strptime(f"{form_date} {form_time}", "%Y-%m-%d %H:%M")
            if raid_datetime < datetime.now():
                errors.append('Raid must be in future')
            else:
                try:
                    raid_event = self.raids_resource.create_raid(raid_name=form['name'], raid_datetime=raid_datetime,
                                                                 guild_id=self.raidteam.guild_id,
                                                                 team_name=self.raidteam.name)
                except InvalidInputException as e:
                    errors.append(e.message)
        return raid_event, errors

    def show(self, guild_id, team_name, raid_name, raid_datetime):
        raid = self.raids_resource.get_raid(raid_name=raid_name, raid_datetime=raid_datetime, guild_id=guild_id,
                                            team_name=team_name)
        return render_template('raid/show.html', raid=raid)
