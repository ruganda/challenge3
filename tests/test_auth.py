from test_base import TestBase
import unittest
from flask import json
import psycopg2



class TestAuth(TestBase):
    
    connection = psycopg2.connect(
            "dbname='ride_db' user='postgres' host='localhost' password='15december' port ='5432'")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE username = %s", ('username',))
    connection.commit()
    connection.close()
    def test_register_valid_details(self):
        """ Tests creating a new user with valid details """
        user = {
            'name': 'test user',
            'username': 'username',
            'password': 'password'
        }
        response = self.client.post('/api/v1/register',
                                    data=json.dumps(user),
                                    content_type='application/json')
        self.assertIn('You registered successfully. Please login.', str(response.data))
        self.assertEqual(response.status_code, 201)
        
        
    def test_register_existing_user(self):
        """ Tests creating a new user with existing username """
        self.create_valid_user()
        response = self.create_valid_user()
        self.assertEqual(response.status_code, 202)
        self.assertIn("User already exists. Please login.", str(response.data))
        self.delete_valid_user()
    
    def test_login_valid_credentials(self):
        """ Tests login with valid credentials """
        self.create_valid_user()
        user = {
            'username': 'validuser',#credentials for valid user , defined in test_base.py
            'password': 'password' 
        }
        response = self.client.post('/api/v1/login', data=json.dumps(user),
                                    content_type='application/json')
        
        self.assertIn('You logged in successfully.', str(response.data))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertTrue(data['token'])
        self.delete_valid_user()

    def test_login_wrong_valid_credentials(self):
        """ Tests login with invalid credentials """
        user = {
            'name': 'right user',
            'username': 'rightuser',
            'password': 'rightpassword'
        }
        self.client.post('/api/v1/register',
                                    data=json.dumps(user),
                                    content_type='application/json')
        user_login = {
            'username': 'rightuser',
            'password': 'wrongpassword' 
        }
        response = self.client.post('/api/v1/login', data=json.dumps(user_login),
                                    content_type='application/json')
        
        self.assertIn('Invalid username or password, Please try again.', str(response.data))
        self.assertEqual(response.status_code, 401)
        
