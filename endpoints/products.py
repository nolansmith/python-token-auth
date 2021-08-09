from constants.error_messages import ERROR_ADDING_PRODUCTS, ERROR_ADDING_SUPPLIERS
from common.responses import json_response
from common.exceptions import print_exception
from flask import jsonify, Blueprint, Response
from flask_cors import cross_origin
from models.product import Product
from models.supplier import Supplier
from schemas.product_schema import ProductSchema
from schemas.supplier_schema import SupplierSchema
from data.mock import PRODUCTS, SUPPLIERS

try:
    from app import db
except ImportError:
    from __main__ import db

product_routes = Blueprint('product_routes', __name__)


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

supplier_schema = SupplierSchema()
suppliers_schema = SupplierSchema(many=True)

@product_routes.route('/products', methods=['GET'])
@cross_origin()
def get_all_products():
    products = Product.query.all()
    result = products_schema.dump(products)
    return jsonify(result)

@product_routes.route('/products/supplier/<supplier_id>', methods=['GET'])
@cross_origin()
def get_all_products_by_supplier_id(supplier_id):
    products = Product.query.filter(Product.supplier_id == int(supplier_id))
    results = products_schema.dump(products)
    return jsonify(results)


@product_routes.route('/suppliers', methods=['GET'])
@cross_origin()
def get_all_suppliers():
    suppliers = Supplier.query.all()
    result = suppliers_schema.dump(suppliers)
    return jsonify(result)

@product_routes.route('/supplier/<supplier_id>', methods=['GET'])
@cross_origin()
def get_supplier_by_supplier_id(supplier_id):
    supplier = Supplier.query.get(supplier_id)

    if supplier is None:
        return Response(status=404)
    return supplier_schema.jsonify(supplier)

  
@product_routes.route('/products/create', methods=['GET'])
@cross_origin()
def create_suppliers_and_products():
    sc = 0
    pc = 0

    for supplier in SUPPLIERS:
        try:
            new_supplier = Supplier(supplier)
            db.session.add(new_supplier)
            db.session.commit()
            sc = sc + 1
        except:
            return json_response(ERROR_ADDING_SUPPLIERS, 500)

    for product in PRODUCTS:

        try:
            new_product= Product(product)
            db.session.add(new_product)
            db.session.commit()
            pc = pc + 1
        except Exception as ex:
            print_exception(ex)
            return json_response(ERROR_ADDING_PRODUCTS, 500)
    
    return 'Created {} suppliers, and {} products'.format(sc, pc)

