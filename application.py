import sys
from pathlib import Path
cwd = Path(__file__).parent / 'src'
sys.path.append(str(cwd))
import os
from flask import Flask
from src.webapp.admin import create_admin_blueprint

# EB looks for an 'application' callable by default.
application = Flask(__name__)
app_env = os.getenv("APP_ENV")
app_url = os.getenv("APP_URL")
application.config["DISCORD_CLIENT_ID"] = os.getenv("DISCORD_CLIENT_ID")
application.config["DISCORD_CLIENT_SECRET"] = os.getenv("DISCORD_CLIENT_SECRET")
application.config["DISCORD_BOT_TOKEN"] = os.getenv("DISCORD_BOT_TOKEN")
application.config["DISCORD_REDIRECT_URI"] = f"{app_url}/discord/redirect"
application.register_blueprint(create_admin_blueprint(application))
application.secret_key = os.getenv("API_KEY")
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
