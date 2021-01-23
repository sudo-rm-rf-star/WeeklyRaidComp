from flask import render_template, redirect, url_for, request
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from .controllers.ControllerFactory import ControllerFactory
import os


def run(app):
    app.secret_key = os.getenv("API_KEY")
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
    app.config["DISCORD_CLIENT_ID"] = os.getenv("DISCORD_CLIENT_ID")
    app.config["DISCORD_CLIENT_SECRET"] = os.getenv("DISCORD_CLIENT_SECRET")
    app.config["DISCORD_BOT_TOKEN"] = os.getenv("DISCORD_BOT_TOKEN")
    app.config["DISCORD_REDIRECT_URI"] = "http://localhost:5000/discord/redirect"
    discord_session = DiscordOAuth2Session(app)

    def raid_controller():
        return ControllerFactory(discord_session).create_raid_controller()

    def home_controller():
        return ControllerFactory(discord_session).create_home_controller()

    def player_controller():
        return ControllerFactory(discord_session).create_player_controller()

    @app.route('/')
    def home():
        if discord_session.authorized:
            return render_template('home.html')
        else:
            return render_template('guest.html')

    @app.route('/raids', methods=["GET", "POST"])
    @requires_authorization
    def raids():
        if request.method == "GET":
            return raid_controller().index()

        return raid_controller().store(request.form)

    @app.route('/raids/create')
    @requires_authorization
    def create_raid():
        return raid_controller().create()

    @app.route('/raids/<name>/<int:timestamp>')
    @requires_authorization
    def raid(name, timestamp):
        return raid_controller().show(name, timestamp)

    @app.route('/raids/<name>/<int:timestamp>/signup-remind', methods=["POST"])
    @requires_authorization
    def signup_remind(name, timestamp):
        return raid_controller().signup_remind(name, timestamp)

    @app.route('/raids/<name>/<int:timestamp>/create-roster', methods=["POST"])
    @requires_authorization
    def create_roster(name, timestamp):
        return raid_controller().create_roster(name, timestamp)

    @app.route('/players')
    @requires_authorization
    def players():
        return player_controller().index()

    @app.route('/players/<int:discord_id>')
    @requires_authorization
    def player(discord_id):
        return player_controller().show(discord_id)

    @app.route("/login/")
    def login():
        return discord_session.create_session()

    @app.route("/logout/")
    def logout():
        discord_session.revoke()
        return redirect(url_for('home'))

    @app.route("/discord/redirect")
    def callback():
        discord_session.callback()
        return redirect(url_for("home"))

    @app.errorhandler(Unauthorized)
    def redirect_unauthorized(e):
        return redirect(url_for("login"))
