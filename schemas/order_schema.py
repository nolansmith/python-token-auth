
from services.ma import ma
from marshmallow import fields


class OrderSchema(ma.Schema):
    id = fields.UUID()
    status = fields.String()
    customer_id = fields.UUID()
    created_on = fields.DateTime()
    updated_on = fields.DateTime()
