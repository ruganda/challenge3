""" Tests module """
import unittest
import psycopg2
from flask import json
from app.models import User, Ride,Request


# from app import create_app,
from app import create_app

class TestBase(unittest.TestCase):
    """ Base class for all test classess """

    app = create_app('TESTING')
    app.app_context().push()
    
    client = app.test_client()
    
    name = 'Muba'
    username = 'ruganda'
    password = 'password'
    
    user = User(name,username, password)

    origin = 'Entebbe'
    destination = 'Rubaga'
    date = "2018-10-10"
    


    valid_user = {
        'name': 'Test User',
        'username': 'validuser',
        'password': 'password'
    }
    
    valid_ride = {
        'origin': 'An origin',
        'destination': "A destination",
        'date': '2018-12-12'     
    }

    

    def setUp(self):
        self.create_valid_user()

    def create_valid_user(self):
        response = self.client.post('/api/v1/register',
                                    data=json.dumps(self.valid_user),
                                    content_type='application/json')
        return response

    def delete_valid_user(self):
        connection = psycopg2.connect(
            "dbname='ride_db' user='postgres' host='localhost' password='15december' port ='5432'")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE username = %s", (self.valid_user['username'],))
        connection.close()

        
    def get_token(self):
        response = self.client.post('/api/v1/login',
                                    data=json.dumps(self.valid_user),
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        return data['token']

    def create_valid_ride(self):
        """ Creates a valid ride to be used for tests """
        response = self.client.post('api/v1/rides/',
                                    data=json.dumps(self.valid_ride),
                                    content_type='application/json',
                                    headers={'Authorization':
                                             self.get_token()})
        return response

    def delete_valid_ride(self):
        """ Deletes the valid ride after tests """
        connection = psycopg2.connect(
            "dbname='ride_db' user='postgres' host='localhost' password='15december' port ='5432'")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM rides WHERE origin = %s", (self.valid_ride['origin'],))
        connection.close()
        


    def tearDown(self):
        self.delete_valid_user()
        self.delete_valid_ride()