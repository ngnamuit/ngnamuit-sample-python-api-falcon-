import falcon
from config import Base, db, api, session, conn
from controllers.users import UserLogin
from controllers.customers import Customer
from models.customers import Customers
from datetime import datetime

def start():
    Customers() ## define table
    Base.metadata.create_all(db)
    api.add_route('/customer/get/{customer_id}', Customer())
    api.add_route('/customer/update', Customer())
    api.add_route('/customer/add', Customer())
    api.add_route('/customer/delete', Customer())
    api.add_route('/user/login', UserLogin())
    return api

api = start()
