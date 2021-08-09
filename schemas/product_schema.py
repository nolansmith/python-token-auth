from services.ma import ma
from marshmallow import fields
from .supplier_schema import SupplierSchema

class ProductSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String()
    supplier_id = fields.Integer()
    supplier = fields.Nested(SupplierSchema)
