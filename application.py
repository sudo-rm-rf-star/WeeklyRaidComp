import sys
from pathlib import Path
cwd = Path(__file__).parent / 'src'
sys.path.append(str(cwd))
import os
from flask import Flask
from src.webapp.admin import admin

# EB looks for an 'application' callable by default.
application = Flask(__name__)
application.register_blueprint(admin)
application.secret_key = os.getenv("API_KEY")
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
