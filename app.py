import falcon
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime
from sqlalchemy.sql import select, insert
from config import Base, db, api, session, conn
from controllers.users import UserLogin
from datetime import datetime
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

class Customer:
	def on_get(self, req, resp, customer_id=-1):
		try:
			if not customer_id or customer_id == -1:
				resp.status = falcon.HTTP_400
				resp.media = {"message": "customer_id field missing"}
				return resp
			query = select([Customers.id, Customers.name, Customers.dob, Customers.updated_at]).\
						where(Customers.id == customer_id)
			result = session.execute(query)
			row = result.fetchone()
			quote = {}
			if row:
				resp.media = {
					'id': row[0],
					'name': row[1],
					'dob': row[2] and row[2].strftime("%Y-%m-%d") or '',
					'updated_at': row[3] and row[3].strftime("%Y-%m-%d %H:%M:%S") or ''
				}
			else:
				resp.status = falcon.HTTP_400
				resp.media = {"message": "Can not find this customer_id in the system"}
		except KeyError as e:
			resp.status = falcon.HTTP_500
			resp.media = {"message": str(e)}
		except Exception as e:
			resp.status = falcon.HTTP_500
			resp.media = {"message": str(e)}

	def on_post(self, req, resp):
		try:
			input = req.media
			dict_value = {"updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
			if not input or not input.get('id', '') or\
				('name' not in input and 'dob' not in input):
				resp.status = falcon.HTTP_400
				resp.media = {"message": "Can not find customer_id, name, dob on payload"}
				return resp
			if 'name' in input:
				dict_value['name'] = input['name']
			if 'dob' in input:
				dict_value['dob'] = input['dob']
			customer = session.query(Customers).filter(Customers.id == input["id"]).\
								update(dict_value)
			if customer:
				session.commit()
				session.flush()
			else:
				resp.status = falcon.HTTP_400
				resp.media = {"message": "Can not find this id in the system"}
				return resp
			resp.media = {
				'id': input['id'],
				'message': 'Record updated is success'
			}

		except KeyError as e:
			session.rollback()
			resp.status = falcon.HTTP_500
			resp.media = {"message": str(e)}
		except Exception as e:
			session.rollback()
			resp.status = falcon.HTTP_500
			resp.media = {"message": str(e)}

	def on_put(self, req, resp):
		try:
			input = req.media
			name = input.get('name', '')
			dob = input.get('dob', '')
			updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			if not name or not dob:
				resp.status = falcon.HTTP_400
				resp.media = {"message": "name, dob is required"}
				return resp
			query = insert(Customers)
			values = {
				'name': name,
				'updated_at': updated_at
			}
			if dob:
				values['dob'] = dob
			customer = Customers(name="%s" % (name), dob="%s"%(dob), updated_at="%s" % (updated_at))
			session.add(customer)
			session.commit()
			resp.media = {
				'id': customer.id,
				'name': customer.name,
				'dob': customer.dob and customer.dob.strftime("%Y-%m-%d") or '',
				'updated_at': customer.updated_at and customer.updated_at.strftime("%Y-%m-%d %H:%M:%S") or ''
			}
		except KeyError as e:
			session.rollback()
			resp.status = falcon.HTTP_500
			resp.media = {"message": str(e)}
		except Exception as e:
			session.rollback()
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

			customer = session.query(Customers).filter(Customers.id == input["id"]).delete()
			if customer:
				session.commit()
				session.flush()
			else:
				resp.status = falcon.HTTP_400
				resp.media = {"message": "Can not find this id in the system"}
				return resp
			resp.media = {
				'id': input['id'],
				'message': 'Record deleted is success'
			}
		except KeyError as e:
			session.rollback()
			resp.status = falcon.HTTP_500
			resp.media = {"message": str(e)}
		except Exception as e:
			session.rollback()
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
    api.add_route('/user/login', UserLogin())
    return api

api = start()
