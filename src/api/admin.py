from flask import redirect, url_for, request, Blueprint
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

from .controllers.RaidController import RaidController


def create_admin_blueprint(app):
    raid_controller = RaidController()
    admin = Blueprint('admin', __name__,
                      template_folder='api/templates',
                      static_folder='api/static',
                      root_path='src')

    @admin.route('/')
    def home():
        return {'data': 'Hello World!'}

    @admin.route('/raids/<int:guild_id>/<team_name>', methods=["GET", "POST"])
    def raids(guild_id, team_name):
        if request.method == "GET":
            return raid_controller.index(guild_id=guild_id, team_name=team_name)

        if request.method == "POST":
            return raid_controller.store(guild_id=guild_id, team_name=team_name, form=request.form)

    @admin.route('/raids/<int:guild_id>/<team_name>/<raid_name>/<int:raid_datetime>', methods=["GET", "PUT"])
    def raid(guild_id, team_name, raid_name, raid_datetime):
        if request.method == "GET":
            return raid_controller.get(guild_id=guild_id, team_name=team_name, raid_name=raid_name,
                                       raid_datetime=raid_datetime)

        if request.method == "PUT":
            return raid_controller.update(data=request.json)

    return admin
