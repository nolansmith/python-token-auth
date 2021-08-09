from services.ma import ma
from marshmallow import fields
from .user_schema import UserSchema
from .order_schema import OrderSchema

class CustomerSchema(ma.Schema):
    id = fields.UUID()
    user_profile = fields.Nested(UserSchema)
    orders = fields.List(fields.Nested(OrderSchema))
