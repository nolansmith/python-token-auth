from flask.blueprints import Blueprint
from .customer import customer_routes
from .order import order_routes
from .products import product_routes
from .token import token_routes

ENDPOINTS: list[Blueprint] = [customer_routes, order_routes, product_routes, token_routes]