import sys
from pathlib import Path
cwd = Path(__file__).parent / 'src'
sys.path.append(str(cwd))
from flask_assets import Environment, Bundle
from flask_feather import Feather

import os
from flask import Flask
from src.webapp.admin import create_admin_blueprint

# EB looks for an 'application' callable by default.
application = Flask(__name__)
application.secret_key = os.getenv("API_KEY")
os.environ['TZ'] = 'Europe/Brussels'
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = str(os.getenv('APP_ENV') == 'production')

application.config["DISCORD_CLIENT_ID"] = os.getenv("DISCORD_CLIENT_ID")
application.config["DISCORD_CLIENT_SECRET"] = os.getenv("DISCORD_CLIENT_SECRET")
application.config["DISCORD_BOT_TOKEN"] = os.getenv("DISCORD_BOT_TOKEN")
application.config["DISCORD_REDIRECT_URI"] = f"{os.getenv('APP_URL')}/discord/redirect"
application.register_blueprint(create_admin_blueprint(application))

# Tailwind CSS bundle
assets = Environment(application)
assets.config[
    "POSTCSS_BIN"
] = f"{Path(__file__).parent.absolute()}/node_modules/.bin/postcss"

tailwindcss = Bundle(
    "css/tailwind.css", filters="postcss", output="dist/css/tailwind.css"
)
assets.register("tailwindcss", tailwindcss)

# Flask-feather
feather = Feather()
feather.init_app(application)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.run()
    application.debug = str(os.getenv('APP_ENV') == 'production')
