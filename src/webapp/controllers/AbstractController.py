from logic.Player import Player
from logic.RaidTeam import RaidTeam
from flask import render_template, redirect, url_for
from flask_discord import DiscordOAuth2Session
import discord


class AbstractController:
    def __init__(self, *args, session: DiscordOAuth2Session, user: discord.User, player: Player, raidteam: RaidTeam):
        self.session = session
        self.player = player
        self.user = user
        self.raidteam = raidteam

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
