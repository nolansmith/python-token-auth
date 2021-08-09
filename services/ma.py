
from flask_marshmallow import Marshmallow

try:
    from app import app
except ImportError:
    from __main__ import app

ma = Marshmallow(app)
