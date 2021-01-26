from logic.Player import Player
from logic.Guild import Guild
from persistence.RaidEventsTable import RaidEventsTable
from persistence.PlayersTable import PlayersTable
from persistence.GuildsTable import GuildsTable
from flask import render_template, redirect, url_for
from flask_discord import DiscordOAuth2Session
import discord


class AbstractController:
    def __init__(self, *args, session: DiscordOAuth2Session, discord_guild: discord.Guild, player: Player, guild: Guild,
                 events_table: RaidEventsTable, players_table: PlayersTable, guilds_table: GuildsTable):
        self.session = session
        self.player = player
        self.guild = guild
        self.discord_guild = discord_guild
        self.events_table = events_table
        self.players_table = players_table
        self.guilds_table = guilds_table
        self.guild_id = self.player.selected_guild_id if self.player else None
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
