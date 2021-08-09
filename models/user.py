try:
    from app import db
except ImportError:
    from __main__ import db

import uuid
import bcrypt
from sqlalchemy.dialects.postgresql import UUID
from constants.roles import ROLE_TYPES, CUSTOMER
from common.validators import is_uuid


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True,  default=uuid.uuid4)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    username = db.Column(db.String(20), )
    password = db.Column(db.String(128))
    role = db.Column(db.String(50))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, user) -> None:

        if ('id' in user):
            if is_uuid(user['id']):
                self.id = user['id']

        self.first_name = user['first_name']
        self.last_name = user['last_name']
        self.username = user['username']
        self.role = user['role'] if 'role' in user and user['role'] in ROLE_TYPES else CUSTOMER

    def set_password(self, password):
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(password, salt)
        self.password = hashed_pw.decode('utf-8')

    def check_password(self, password):
        password_match = bcrypt.checkpw(
            password.encode('utf-8'), self.password.encode('utf-8'))
        return password_match

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        pw = password.encode('utf-8')
        hashed_pw = bcrypt.hashpw(pw, salt)
        return hashed_pw

    @property
    def get_id(self):
        return self.id
