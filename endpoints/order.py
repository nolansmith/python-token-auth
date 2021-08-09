
from common.validators import is_uuid
from common.responses import json_response
from common.decorators import auth_required
from flask import Blueprint, request
from flask_cors import cross_origin
from models import Order
from common.responses import json_response
from constants.error_messages import SERVER_ERROR, ORDER_NOT_FOUND, ORDER_BAD_ID_TYPE
from schemas import OrderSchema


try:
    from app import db
except ImportError:
    from __main__ import db

order_routes = Blueprint('order_routes', __name__, url_prefix='/order')

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

@order_routes.route('/create', methods=['POST'])
@cross_origin()
@auth_required
def create_order():
    order = request.json
    new_order = Order(order)

    try:
        db.session.add(new_order)
        db.session.commit()
        return order_schema.jsonify(new_order)
    except:
        return json_response(SERVER_ERROR, 500)

@order_routes.route('/<id>', methods=['GET'])
@cross_origin()
def get_single_order(id):
   
    if is_uuid(id) is False:
        return json_response(ORDER_BAD_ID_TYPE,500)

    order = Order.query.get(id)

    if order is None:
        return json_response(ORDER_NOT_FOUND, 404)
    
    return order_schema.jsonify(order)

    


