try:
    from app import db
except ImportError:
    from __main__ import db

import uuid
from sqlalchemy.dialects.postgresql import UUID
from common.validators import is_uuid


class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(UUID(as_uuid=True), primary_key=True,  default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    user_profile = db.relationship("User", lazy='joined')
    orders = db.relationship(
        "Order", primaryjoin="Order.customer_id == Customer.id", overlaps="customer", uselist=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, customer) -> None:
        if ('id' in customer):
            if is_uuid(customer['id']):
                self.id = customer['id']

        self.user_id = customer['user_id']

    @property
    def get_user_profile(self):
        return self.user_profile

    @property
    def get_user_id(self):
        return self.user_profile.id
