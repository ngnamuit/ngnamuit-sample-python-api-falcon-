# -*- coding: utf-8 -*-
#!/usr/bin/python
import falcon
import ConfigParser as configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import argparse
from authmiddleware import AuthMiddleware

config = configparser.ConfigParser()
config.read('config.ini')
DatabaseHost = config.get('DEFAULT', 'DatabaseHost') or ''
DatabaseName = config.get('DEFAULT', 'DatabaseName') or ''
DatabaseUserName = config.get('DEFAULT', 'DatabaseUserName') or ''
DatabasePassword = config.get('DEFAULT', 'DatabasePassword') or ''
JWT_SECRET_KEY = config.get('DEFAULT', 'JWT_SECRET_KEY') or ''
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://%s:%s@%s/%s'%(
    DatabaseUserName, DatabasePassword, DatabaseHost, DatabaseName)
db = create_engine(SQLALCHEMY_DATABASE_URI)
session_factory = sessionmaker(bind=db)
Base = declarative_base()

class SQLAlchemySessionManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def process_resource(self, req, resp, resource, params):
        resource.session = scoped_session(self.session_factory)

    def process_response(self, req, resp, resource, req_succeeded):
        if hasattr(resource, 'session'):
            resource.session.remove()
######
api = falcon.API(middleware=[AuthMiddleware(), SQLAlchemySessionManager(session_factory)])
