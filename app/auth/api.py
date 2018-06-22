
from flask.views import MethodView
from flask import jsonify, request, abort, make_response
from app.models import User
import jwt
import datetime


class RegistrationView(MethodView):
    """This class-based view registers a new user."""

    def post(self):
        """registers a user"""
        data = request.json
        # Query to see if the user already exists
        user_object = User(data['name'],data['username'],data['password'])
        user = user_object.get_single_user(data['username'])
        print(user)
        if not user:
            try:
                # Register the user
                name = data['name']
                username = data['username']
                password = data['password']
                user = User(name=name, username=username, password=password)
                user.insert_data(user)

                response = {
                    'message': 'You registered successfully. Please login.',
                }
                return make_response(jsonify(response)), 201

            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'message': 'User already exists. Please login.'
            }

            return make_response(jsonify(response)), 202


class LoginView(MethodView):
    """This class-based view handles user login and access token generation."""

    def post(self):
        '''Logs in a registered user'''
        data = request.json
        try:
            user = User(data['username'],data['password'])
            user_object = user.get_single_user(data['username'])
            user = User(username=user_object[2], password=user_object[3])
            
            if user.username == data['username'] and user.password == data['password']:
                # Generate the access token
                token=jwt.encode({'username': user.username, 'exp': datetime.datetime.utcnow()
                            + datetime.timedelta(minutes=60)}, 'donttouch')
                if token:
                    response={
                        'message': 'You logged in successfully.',
                        'token': token.decode('UTF-8')
                    }
                    return make_response(jsonify(response)), 200
            else:
                
                response = {
                    'message': 'Invalid username or password, Please try again.'
                }
                return make_response(jsonify(response)), 401

        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500




