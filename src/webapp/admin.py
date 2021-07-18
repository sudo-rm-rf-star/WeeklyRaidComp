from flask import redirect, url_for, request, Blueprint
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from .controllers.ControllerFactory import ControllerFactory


def create_admin_blueprint(app):
    admin = Blueprint('admin', __name__,
                      template_folder='webapp/templates',
                      static_folder='webapp/static',
                      root_path='src')

    discord_session = DiscordOAuth2Session(app=app)

    def raid_controller():
        return ControllerFactory(discord_session).create_raid_controller()

    def home_controller():
        return ControllerFactory(discord_session).create_home_controller()

    def player_controller():
        return ControllerFactory(discord_session).create_player_controller()

    def guild_controller():
        return ControllerFactory(discord_session).create_guild_controller()

    @admin.route('/raids/<int:guild_id>/<team_name>', methods=["GET", "POST"])
    @requires_authorization
    def raids(guild_id, team_name):
        if request.method == "GET":
            return raid_controller().index(guild_id=guild_id, team_name=team_name)

        if request.method == "POST":
            return raid_controller().store(request.form)

    @admin.route('/raids/<int:guild_id>/<team_name>/<raid_name>/<int:raid_datetime>', methods=["GET", "PUT"])
    @requires_authorization
    def raid(guild_id, team_name, raid_name, raid_datetime):
        if request.method == "GET":
            return raid_controller().get(guild_id=guild_id, team_name=team_name, raid_name=raid_name, raid_datetime=raid_datetime)

        if request.method == "PUT":
            return raid_controller().store(request.form)

    @admin.route("/login/")
    def login():
        return discord_session.create_session()

    @admin.route("/logout/")
    def logout():
        discord_session.revoke()
        return {'data': discord_session.get_authorization_token()}

    @admin.route("/discord/redirect")
    def callback():
        discord_session.callback()
        return redirect("http://localhost:5000")

    @admin.errorhandler(Unauthorized)
    def redirect_unauthorized(e):
        # TODO
        return {'error': "UNAUTHORIZED"}, 403

    return admin
