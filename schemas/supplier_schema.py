from services.ma import ma
from marshmallow import fields

class SupplierSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String()
