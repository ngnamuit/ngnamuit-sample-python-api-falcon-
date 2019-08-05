# -*- coding: utf-8 -*-
#!/usr/bin/python
import jwt
import falcon

class AuthMiddleware:
    def process_request(self, req, resp):
        try:
            if req.path in ('/user/login', '/user/login/'):
                return
            token = req.get_header('Authorization')
            challenges = ['Token type="Fernet"']

            if token is None:
                description = ('Please provide an auth token '
                               'as part of the request.')

                raise falcon.HTTPUnauthorized('Auth token required',
                                              description,
                                              challenges,
                                              href='http://docs.example.com/auth')
            token_jwt = token.replace('Bearer ','').strip()
            user_decoded = jwt.decode(token_jwt, JWT_SECRET_KEY, algorithms=['HS256'])
            is_valid_user = check_user(user_decoded.get('user_name', ''), user_decoded.get('password', ''))
            if not is_valid_user:
                description = ('The provided auth token is not valid. '
                               'Please request a new token and try again.')

                raise falcon.HTTPUnauthorized('Authentication required',
                                              description,
                                              challenges,
                                              href='http://docs.example.com/auth')
        except Exception as e:
            raise falcon.HTTPUnauthorized('Authentication required',
                                          (str(e)),
                                          challenges,
                                          href='http://docs.example.com/auth')
