import sys
from pathlib import Path
from flask import Flask
from src.webapp.flask import run

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    cwd = Path(__file__).parent / 'src'
    sys.path.append(str(cwd))
    application.debug = True
    run(application)
