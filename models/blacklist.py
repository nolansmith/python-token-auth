try:
    from app import db
except ImportError:
    from __main__ import db

from enum import unique
from common.exceptions import print_exception
import uuid
from sqlalchemy.dialects.postgresql import UUID


class BlacklistToken(db.Model):
    __tablename__ = 'blacklist_tokens'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = db.Column(db.String(256), )
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, token: str) -> None:
        self.token = token

    def add_token_to_blacklist(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print_exception(e)
            return False
    
    @staticmethod
    def check_for_blacklist(token: str):
        token = BlacklistToken.query.filter(BlacklistToken.token == token).first()
        if token is not None:
            return True
        else:
            return False
    



   
