from logic.Player import Player
from logic.Guild import Guild
from persistence.tables.RaidEventsTable import RaidEventsTable
from persistence.tables.PlayersTable import PlayersTable
from persistence.tables.GuildsTable import GuildsTable
from flask import render_template, redirect, url_for
from flask_discord import DiscordOAuth2Session
from events.EventQueue import EventQueue


class AbstractController:
    def __init__(self, *args, session: DiscordOAuth2Session, player: Player, guild: Guild,
                 raids_table: RaidEventsTable, players_table: PlayersTable, guilds_table: GuildsTable,
                 event_queue: EventQueue):
        self.session = session
        self.player = player
        self.guild = guild
        self.raids_table = raids_table
        self.players_table = players_table
        self.guilds_table = guilds_table
        self.event_queue = event_queue
        self.guild_id = self.guild.id
        self.group_id = self.player.selected_raidgroup_id if self.player else None

    def view_directory(self):
        return ''

    def is_auth(self):
        return self.session.authorized

    def view(self, _name, **kwargs):
        html_file = f'{_name}.html'
        if self.view_directory():
            html_file = f'{self.view_directory()}/{html_file}'
        return render_template(html_file, **kwargs)

    def redirect(self, _name, **kwargs):
        return redirect(url_for(_name, **kwargs))
