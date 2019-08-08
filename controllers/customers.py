# -*- coding: utf-8 -*-
#!/usr/bin/python
import falcon
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime
from sqlalchemy.sql import select, insert
import config
from controllers.users import UserLogin
from models.customers import Customers
from datetime import datetime

class Customer():
	def on_get(self, req, resp, customer_id=-1):
		try:
			if '/customer/get/' not in req.path:
				resp.status = falcon.HTTP_405
				return resp
			if not customer_id or customer_id == -1:
				resp.status = falcon.HTTP_400
				resp.media = {"message": "customer_id field missing"}
				return resp
			query = select([Customers.id, Customers.name, Customers.dob, Customers.updated_at]).\
						where(Customers.id == customer_id)
			result = config.session.execute(query)
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
			if '/customer/update' not in req.path:
				resp.status = falcon.HTTP_405
				return resp
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
			customer = config.session.query(Customers).filter(Customers.id == input["id"]).\
								update(dict_value)
			if customer:
				config.session.commit()
				config.session.flush()
			else:
				resp.status = falcon.HTTP_400
				resp.media = {"message": "Can not find this id in the system"}
				return resp
			resp.media = {
				'id': input['id'],
				'message': 'Record updated is success'
			}

		except KeyError as e:
			config.session.rollback()
			resp.status = falcon.HTTP_500
			resp.media = {"message": str(e)}
		except Exception as e:
			config.session.rollback()
			resp.status = falcon.HTTP_500
			resp.media = {"message": str(e)}

	def on_put(self, req, resp):
		try:
			if '/customer/add' not in req.path:
				resp.status = falcon.HTTP_405
				return resp
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
			config.session.add(customer)
			config.session.commit()
			resp.media = {
				'id': customer.id,
				'name': customer.name,
				'dob': customer.dob and customer.dob.strftime("%Y-%m-%d") or '',
				'updated_at': customer.updated_at and customer.updated_at.strftime("%Y-%m-%d %H:%M:%S") or ''
			}
		except KeyError as e:
			config.session.rollback()
			resp.status = falcon.HTTP_500
			resp.media = {"message": str(e)}
		except Exception as e:
			config.session.rollback()
			resp.status = falcon.HTTP_500
			resp.media = {"message": str(e)}

	def on_delete(self, req, resp):
		try:
			if '/customer/delete' not in req.path:
				resp.status = falcon.HTTP_405
				return resp
			input = req.media
			if not input or not input.get('id', '') or \
				('name' not in input and 'dob' not in input):
				resp.status = falcon.HTTP_400
				resp.media = {"message": "Can not find customer_id, name, dob on payload"}
				return resp

			customer = config.session.query(Customers).filter(Customers.id == input["id"]).delete()
			if customer:
				config.session.commit()
				config.session.flush()
			else:
				resp.status = falcon.HTTP_400
				resp.media = {"message": "Can not find this id in the system"}
				return resp
			resp.media = {
				'id': input['id'],
				'message': 'Record deleted is success'
			}
		except KeyError as e:
			config.session.rollback()
			resp.status = falcon.HTTP_500
			resp.media = {"message": str(e)}
		except Exception as e:
			config.session.rollback()
			resp.status = falcon.HTTP_500
			resp.media = {"message": str(e)}
