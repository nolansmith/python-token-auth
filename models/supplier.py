from enum import unique


try:
    from app import db
except ImportError:
    from __main__ import db

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True, )
    name = db.Column(db.String(50), )
  

    def __init__(self, supplier) -> None:
        self.name = supplier['name']
        
        
