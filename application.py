import sys
from pathlib import Path
from flask import Flask
from src.webapp.flask import run

# EB looks for an 'application' callable by default.
application = Flask(__name__, root_path=Path(__file__).parent / 'src')

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    run(application)
