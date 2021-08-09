try:
    from app import db
except ImportError:
    from __main__ import db


from common.exceptions import print_exception
from models import Supplier, Product, User, Customer, Order
from data.mock import SUPPLIERS, PRODUCTS, USERS, ORDERS, CUSTOMERS




def create_suppliers_and_products():
    sc = 0
    pc = 0

    for supplier in SUPPLIERS:
        try:
            new_supplier = Supplier(supplier)
            db.session.add(new_supplier)
            db.session.commit()
            sc = sc + 1
        except Exception as ex:
            print_exception(ex)

    for product in PRODUCTS:

        try:
            new_product = Product(product)
            db.session.add(new_product)
            db.session.commit()
            pc = pc + 1
        except Exception as ex:
            print_exception(ex)

    print('Created {} suppliers, and {} products'.format(sc, pc))


def create_users():
    user_count = 0
    for u in USERS:
        user = User(u)
        user.set_password(u['clear_password'].encode('utf-8'))

        try:
            db.session.add(user)
            db.session.commit()
            user_count = user_count + 1
        except Exception as ex:
            print_exception(ex)

    print("Created {} users ".format(user_count))


def create_customers():
    customer_count = 0
    for c in CUSTOMERS:
        try:
            customer = Customer(c)
            db.session.add(customer)
            db.session.commit()
            customer_count = customer_count + 1
        except Exception as ex:
            print_exception(ex)

    print("Created {} customers ".format(customer_count))


def create_orders():
    order_count = 0
    for order in ORDERS:
        new_order = Order(order)

        try:
            db.session.add(new_order)
            db.session.commit()
            order_count = order_count + 1
        except Exception as ex:
            print_exception(ex)

    print("Created {} orders ".format(order_count))


def perform_seed():
    create_suppliers_and_products()
    create_users()
    create_customers()
    create_orders()