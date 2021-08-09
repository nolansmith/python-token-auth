try:
    from app import db
except ImportError:
    from __main__ import db

from constants.order import ORDER_STATUSES, PLACED
import uuid
from sqlalchemy.dialects.postgresql import UUID
from common.validators import is_uuid


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(UUID(as_uuid=True), primary_key=True,
                    default=uuid.uuid4)
    status = db.Column(db.String, nullable=False, default='placed')
    customer_id = db.Column(UUID(as_uuid=True), db.ForeignKey('customers.id'))
    customer = db.relationship("Customer", primaryjoin="Order.customer_id == Customer.id")
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, order: dict) -> None:
        if ('id' in order):
            if is_uuid(order['id']):
                self.id = order['id']

        self.status = order['status'] if 'status' in order and order['status'] in ORDER_STATUSES else PLACED
        self.customer_id = order['customer_id']
