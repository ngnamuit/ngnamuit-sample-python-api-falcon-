# -*- coding: utf-8 -*-
#!/usr/bin/python
from werkzeug.security import safe_str_cmp
from datetime import datetime
from passlib.context import CryptContext
from config import JWT_SECRET_KEY
import falcon
import jwt

users = [
	{
		'id': 1,
		'user_name': 'admin',
		'password': 'admin',
	},
	{
		'id': 2,
		'user_name': 'user',
		'password': '$pbkdf2-sha256$30000$ASAk5DxnzJmzNuacc651bg$HlwuY/SjdoWkT1OMP5k3VkDegU21s0M7lw5rY0QoCDA',
	}
]
pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)
def encrypt_password(password):
    return pwd_context.encrypt(password)

def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)

def check_user(username, password):
    for user in users:
        if user['user_name'] == username and check_encrypted_password(password, user['password']):
            result = user.copy()
            result['password'] = password
            return result
    return False

class UserLogin:
    def on_post(self, req, resp):
        try:
            input = req.media
            username = input.get('username', '')
            password = input.get('password', '')
            if not input:
                resp.status = falcon.HTTP_400
                resp.media = {"message": "Missing JSON in request"}
                return resp
            if not username or not password:
                resp.status = falcon.HTTP_400
                resp.media = {"message": "Missing username or password parameter"}
                return resp
            user = check_user(username, password)
            if user:
                resp.media = {'access_token': jwt.encode(user, JWT_SECRET_KEY, algorithm='HS256')}
                return resp
            resp.status = falcon.HTTP_401
            resp.media = {"message": "Username or password incorrect"}
        except KeyError as e:
			resp.status = falcon.HTTP_500
			resp.media = {"message": str(e)}
        except Exception as e:
			resp.status = falcon.HTTP_500
			resp.media = {"message": str(e)}
