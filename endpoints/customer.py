try:
    from app import db

except ImportError:
    from __main__ import db

from constants.response_messages import LOGOUT_SUCCESSFUL
from models.blacklist import BlacklistToken
from constants.error_messages import BAD_PASSWORD, CUSTOMER_NOT_FOUND, SERVER_ERROR, USER_NOT_FOUND, NOT_ALLOWED
from services.auth.token import create_user_auth_token, get_token_from_header, get_userid_from_token, json_token_response
from common.responses import json_response
from common.exceptions import print_exception
from models.user import User
from flask import Blueprint, request
from flask_cors import cross_origin
from schemas.customer_schema import CustomerSchema
from models.customer import Customer
from schemas.user_schema import UserSchema
from common.decorators.auth import auth_required

customer_routes = Blueprint(
    'customer_routes', __name__, url_prefix='/customer')
user_schema = UserSchema()
customer_schema = CustomerSchema()


@customer_routes.route('/create', methods=['POST'])
@cross_origin()
def create_single_customer():
    new_customer = request.json
    user = User(new_customer)
    user.set_password(new_customer['password'].encode('utf-8'))

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as ex:
        print_exception(ex)
        return json_response(SERVER_ERROR, 500)

    try:
        customer = Customer({"user_id": user.get_id})
        db.session.add(customer)
        db.session.commit()
        return customer_schema.jsonify(customer)

    except Exception as ex:
        print_exception(ex)
        return json_response(SERVER_ERROR, 500)


@customer_routes.route('/login', methods=['POST'])
@cross_origin()
def customer_login():
    # does the customer exist as a user
    customer = request.json
    user = User.query.filter(User.username == customer['username']).first()

    if user is None:
        return json_response(USER_NOT_FOUND, 404)

    if user.check_password(customer['password']) is False:
        return json_response(BAD_PASSWORD, 401)

    customer = Customer.query.filter(Customer.user_id == user.id).first()

    if customer is None:
        return json_response(CUSTOMER_NOT_FOUND)

    token = create_user_auth_token(user_id=customer.get_user_id)
    return json_token_response(token)


@customer_routes.route('/logout', methods=['POST'])
@cross_origin()
@auth_required
def customer_logout():
    token = get_token_from_header()
    blacklisted = BlacklistToken.check_for_blacklist(token)
    
    # burn this token
    if blacklisted == False:
        bl_token = BlacklistToken(token)
        blacklisted = bl_token.add_token_to_blacklist()
        if (blacklisted == False):
                return json_response(SERVER_ERROR, 500)

    return json_response(LOGOUT_SUCCESSFUL, 200, token_added_to_blacklist=blacklisted)


@customer_routes.route('/profile', methods=['GET'])
@cross_origin()
@auth_required
def get_customer_profile():
    try:
        user_id = get_userid_from_token()
        customer = Customer.query.filter(Customer.user_id == user_id).first()

        if customer is None:
            return json_response(NOT_ALLOWED, 403)

        return customer_schema.jsonify(customer)
    except Exception as ex:
        print_exception(ex)
        return json_response(SERVER_ERROR, 500)
