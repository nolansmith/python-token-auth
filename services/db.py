from flask_sqlalchemy import SQLAlchemy
try:
    from app import app
except ImportError:
    from __main__ import app

database = SQLAlchemy(app)
