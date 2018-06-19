import uuid
from datetime import date, datetime
import psycopg2
import uuid


class Ride(object):
    '''  Defines a Ride class'''

    def __init__(self,id=None, origin=None, destination=None, date =None):
        ''' Initializes the ride object'''
        self.id = id
        self.origin = origin
        self.destination = destination
        self.date = date
    
    @classmethod
    def find_by_id(cls, r_id):
        '''Returns a user object with that username'''
        connection = psycopg2.connect(
        "dbname='ride_db' user='postgres' host='localhost' password='15december' port ='5432'")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM rides WHERE id = %(id)s", {'id': r_id})

        row = cursor.fetchone()
        if row:
            ride = {'id': row[0], 'origin': row[1],
                             'destination': row[2], 'date': row[3], "driver": row[4]}
        connection.close()        
        return ride
    
    def insert(self, driver):
        connection = psycopg2.connect(
            "dbname='ride_db' user='postgres' host='localhost' password='15december' port ='5432'")
        cursor = connection.cursor()
        query = "INSERT INTO rides (origin, destination, date, driver) VALUES(%s, %s, %s, %s)"
        cursor.execute(query, (self.origin, self.destination,
                               self.date, driver))

        connection.commit()
        connection.close()

        

    @classmethod
    def fetch_all(self):
        connection = psycopg2.connect(
            "dbname='ride_db' user='postgres' host='localhost' password='15december' port ='5432'")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM rides ")
        rows = cursor.fetchall()
        rides = []
        for row in rows:
            print(row)
            rides.append({'id': row[0], 'origin': row[1],
                             'destination': row[2], 'date': row[3], "driver": row[4]})
        connection.close()
        return rides
   