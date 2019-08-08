from datetime import datetime
import config
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customers(Base):
	__tablename__ = 'customers'
	id = Column(Integer, primary_key=True)
	name = Column(String(256), nullable=False)
	dob = Column(Date)
	updated_at = Column(DateTime)
