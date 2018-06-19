"""This module defines a user class and methods associated to it"""
import os
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import psycopg2
# from create_table import connection


class User:
    table_title = 'users'

    def __init__(self, user_id=0, name=None, username=None, password=None, rides_taken=0, rides_given=0):
        self.user_id = user_id
        self.name = name
        self.username = username
        self.password = password      
        self.rides_taken = rides_taken
        self.rides_given = rides_given

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return check_password_hash(self.password, password)

    @classmethod
    def fetch_by_username(cls, username):
        '''Returns a user object with that username'''
        connection = psycopg2.connect(
        "dbname='ride_db' user='postgres' host='localhost' password='15december' port ='5432'")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username = %(username)s", {'username': username})

        row = cursor.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        print(user)
        return user


    def insert_data(self, user):
        connection = psycopg2.connect(
    "dbname='ride_db' user='postgres' host='localhost' password='15december' port ='5432'")
        cursor = connection.cursor()

        cursor.execute("INSERT INTO users (name, username, password, rides_taken, rides_given) VALUES( %s, %s, %s,%s,%s)",
                       (user.name, user.username, user.password, self.rides_taken, self.rides_given),)
        connection.commit()
        connection.close()

    @classmethod
    def find_by_id(cls, _id):
        connection = psycopg2.connect(
    "dbname='ride_db' user='postgres' host='localhost' password='15december' port ='5432'")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM users WHERE id = %s", [_id])

        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        print(user)
        return user
