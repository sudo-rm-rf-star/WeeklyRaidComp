from flask import redirect, url_for, request, Blueprint
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from .controllers.ControllerFactory import ControllerFactory


def create_admin_blueprint(app):
    admin = Blueprint('admin', __name__, template_folder='webapp/templates', root_path='src')

    discord_session = DiscordOAuth2Session(app=app)

    def raid_controller():
        return ControllerFactory(discord_session).create_raid_controller()

    def home_controller():
        return ControllerFactory(discord_session).create_home_controller()

    def player_controller():
        return ControllerFactory(discord_session).create_player_controller()

    def guild_controller():
        return ControllerFactory(discord_session).create_guild_controller()

    @admin.route('/')
    def home():
        return home_controller().home()

    @admin.route('/guilds')
    @requires_authorization
    def guilds():
        return guild_controller().index()

    @admin.route('/guild/<int:guild_id>')
    @requires_authorization
    def guild(guild_id):
        return guild_controller().show(guild_id)

    @admin.route('/raids', methods=["GET", "POST"])
    @requires_authorization
    def raids():
        if request.method == "GET":
            return raid_controller().index()

        return raid_controller().store(request.form)

    @admin.route('/raids/create')
    @requires_authorization
    def create_raid():
        return raid_controller().create()

    @admin.route('/raids/<name>/<int:timestamp>')
    @requires_authorization
    def raid(name, timestamp):
        return raid_controller().show(name, timestamp)

    @admin.route('/raids/<name>/<int:timestamp>/signup-remind', methods=["POST"])
    @requires_authorization
    def signup_remind(name, timestamp):
        return raid_controller().signup_remind(name, timestamp)

    @admin.route('/raids/<name>/<int:timestamp>/create-roster', methods=["POST"])
    @requires_authorization
    def create_roster(name, timestamp):
        return raid_controller().create_roster(name, timestamp)

    @admin.route('/players')
    @requires_authorization
    def players():
        return player_controller().index()

    @admin.route('/player/<int:discord_id>')
    @requires_authorization
    def player(discord_id):
        return player_controller().show(discord_id)

    @admin.route("/login/")
    def login():
        return discord_session.create_session()

    @admin.route("/logout/")
    def logout():
        discord_session.revoke()
        return redirect(url_for('.home'))

    @admin.route("/discord/redirect")
    def callback():
        discord_session.callback()
        return redirect(url_for(".home"))

    @admin.errorhandler(Unauthorized)
    def redirect_unauthorized(e):
        return redirect(url_for(".login"))

    return admin
