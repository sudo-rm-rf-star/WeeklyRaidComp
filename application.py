import sys
from pathlib import Path

cwd = Path(__file__).parent / 'src'
sys.path.append(str(cwd))
from api.controllers.RaidController import RaidController

import os
from flask import Flask, request
from flask_cors import CORS

# EB looks for an 'application' callable by default.
app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("API_KEY")
os.environ['TZ'] = 'Europe/Brussels'
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = str(os.getenv('APP_ENV') == 'production')

app.config["DISCORD_CLIENT_ID"] = os.getenv("DISCORD_CLIENT_ID")
app.config["DISCORD_CLIENT_SECRET"] = os.getenv("DISCORD_CLIENT_SECRET")
app.config["DISCORD_BOT_TOKEN"] = os.getenv("DISCORD_BOT_TOKEN")
app.config["DISCORD_REDIRECT_URI"] = f"{os.getenv('APP_URL')}/discord/redirect"

raid_controller = RaidController()


@app.route('/')
def home():
    return {'data': 'Hello World!'}


@app.route('/raids/<token>', methods=["GET"])
def raid(token):
    return raid_controller.get(token=token)


@app.route('/raids/<token>/roster', methods=["PUT"])
def update_roster(token):
    return raid_controller.publish_roster_changes(token, request.get_json())


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.run(host="0.0.0.0")
    app.debug = str(os.getenv('APP_ENV') == 'production')
