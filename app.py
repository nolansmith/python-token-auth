
from constants.error_messages import RESOURCE_NOT_FOUND
from common.responses import json_response
from flask import Flask
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_pyfile('settings.py')
from services.db import database

db = database

from endpoints import ENDPOINTS
import models

migrate = Migrate(app, db)

for ep in ENDPOINTS:
    app.register_blueprint(ep)

from services.seed import perform_seed


@app.cli.command("seed-db")
def seed_db():
    perform_seed()

@app.errorhandler(404)
@app.errorhandler(405)
def handle_the_error(ex):
    # handle all other routes here
    return json_response(RESOURCE_NOT_FOUND)


if __name__ == "__main__":
    app.run(debug=True)