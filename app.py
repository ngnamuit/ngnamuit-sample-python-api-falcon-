import falcon
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime
from config import Base, db, api

class Customer:
	def __init__(self):
		print "init === ",self

	def on_get(self, req, resp, customer_id=-1):
		try:
			if not customer_id or customer_id == -1:
				resp.status = falcon.HTTP_400
				resp.media = {"message": "customer_id field missing"}
				return resp
			quote = {
				'quote': (
					"I've always been more interested in "
					"the future than in the past."
				),
				'author': 'Grace Hopper'
			}
			resp.media = quote
		except KeyError as e:
			resp.status = falcon.HTTP_500
			resp.media = {"message": str(e)}
		except Exception as e:
			resp.status = falcon.HTTP_500
			resp.media = {"message": str(e)}

	def on_post(self, req, resp):
		try:
			input = req.media
			if not input or not input.get('id', '') or\
				('name' not in input and 'dob' not in input):
				resp.status = falcon.HTTP_400
				resp.media = {"message": "Can not find customer_id, name, dob on payload"}
				return resp
			resp.media = {}
		except KeyError as e:
			resp.status = falcon.HTTP_500
			resp.media = {"message": str(e)}
		except Exception as e:
			resp.status = falcon.HTTP_500
			resp.media = {"message": str(e)}

	def on_put(self, req, resp):
		try:
			input = req.media
			if not input or not input.get('id', '') or \
				('name' not in input and 'dob' not in input):
				resp.status = falcon.HTTP_400
				resp.media = {"message": "Can not find customer_id, name, dob on payload"}
				return resp
			resp.media = {}
		except KeyError as e:
			resp.status = falcon.HTTP_500
			resp.media = {"message": str(e)}
		except Exception as e:
			resp.status = falcon.HTTP_500
			resp.media = {"message": str(e)}

	def on_delete(self, req, resp):
		try:
			input = req.media
			if not input or not input.get('id', '') or \
				('name' not in input and 'dob' not in input):
				resp.status = falcon.HTTP_400
				resp.media = {"message": "Can not find customer_id, name, dob on payload"}
				return resp
			resp.media = {}
		except KeyError as e:
			resp.status = falcon.HTTP_500
			resp.media = {"message": str(e)}
		except Exception as e:
			resp.status = falcon.HTTP_500
			resp.media = {"message": str(e)}

class Customers(Base):
	__tablename__ = 'customers'
	id = Column(Integer, primary_key=True)
	name = Column(String(256), nullable=False)
	dob = Column(Date)
	updated_at = Column(DateTime)

def start():
    Base.metadata.create_all(db)
    api.add_route('/customer/get/{customer_id}', Customer())
    api.add_route('/customer/update', Customer(), alias='update')
    api.add_route('/customer/add', Customer())
    api.add_route('/customer/delete', Customer())
    return api

api = start()
