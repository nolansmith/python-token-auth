from enum import unique


try:
    from app import db
except ImportError:
    from __main__ import db

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, )
    name = db.Column(db.String(30), )
    supplier_id = db.Column(db.Integer,db.ForeignKey('suppliers.id'))
    supplier = db.relationship("Supplier", lazy='joined')

    def __init__(self, product) -> None:
        self.name = product['name']
        self.supplier_id = product['supplier_id']
        
