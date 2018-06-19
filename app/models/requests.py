'''This module handles the Request class '''
import psycopg2
class Request(object):
    ''' Defines the Request class'''

    def __init__(self):  
        pass
    @classmethod
    def insert(cls,ride_id, passenger):
        connection = psycopg2.connect(
            "dbname='ride_db' user='postgres' host='localhost' password='15december' port ='5432'")
        cursor = connection.cursor()
        query = "INSERT INTO requests (ride_id, passenger) VALUES(%s, %s)"
        cursor.execute(query, (ride_id, passenger))

        connection.commit()
        connection.close()
