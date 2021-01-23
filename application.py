from flask import Flask
from webapp.flask import run

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    run(application)
