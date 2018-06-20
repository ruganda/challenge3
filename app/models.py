
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import psycopg2
class Database():
    """This class does all database related staff"""
    database_name = 'ride_db'
    conn = psycopg2.connect("dbname='{}' user='postgres' host = 'localhost' password='15december' port='5432'".format(database_name))
    cur =  conn.cursor()

    # def __init__(self, database_name = 'ride_db'):
    #     # self.conn = psycopg2.connect("dbname='{}' user='postgres' host = 'localhost' password='15december' port='5432'".format(database_name))
    #     # self.cur = self.conn.cursor()
    #     pass
class User(Database):
    table_title = 'users'
    
    def __init__(self, user_id=0, name=None, username=None, password=None, rides_taken=0, rides_given=0):
        Database.__init__(self)
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
        '''Returns a user object associated to  that username'''
        # conn = psycopg2.connect("dbname='ride_db' user='postgres' host = 'localhost' password='15december' port='5432'")
        # cls.cur =  conn.cursor() 
        cls.cur.execute(
            "SELECT * FROM users WHERE username = %s", ('user',))

        row = cls.cur.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        return user


    def insert_data(self, user):
        """Adds a new record to the database"""
    
        self.cur.execute("INSERT INTO users (name, username, password, rides_taken, rides_given) VALUES( %s, %s, %s,%s,%s)",
                       (user.name, user.username, user.password, self.rides_taken, self.rides_given),)
        self.conn.commit()
        

    @classmethod
    def find_by_id(cls, _id):
        result = cls.cur.execute("SELECT * FROM users WHERE id = %s", [_id])

        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        cls.conn.close()
        return user

class Ride(Database):
    '''  Defines a Ride class'''

    def __init__(self,id=None, origin=None, destination=None, date =None):
        ''' Initializes the ride object'''
        self.instance = Database.__init__(self)
        self.id = id
        self.origin = origin
        self.destination = destination
        self.date = date
    
    @classmethod
    def find_by_id(cls, r_id):
        cls.cur.execute(
            "SELECT * FROM rides WHERE id = %(id)s", {'id': r_id})

        row = cls.cur.fetchone()
        if row:
            ride = {'id': row[0], 'origin': row[1],
                             'destination': row[2], 'date': row[3], "driver": row[4]}
        cls.conn.close()        
        return ride
    
    def insert(self, driver):
        
        query = "INSERT INTO rides (origin, destination, date, driver) VALUES(%s, %s, %s, %s)"
        self.cur.execute(query, (self.origin, self.destination,
                               self.date, driver))
        self.conn.commit()
      

        

    @classmethod
    def fetch_all(cls):
        """ Fetches all ride recods from the database"""
        cls.cur.execute("SELECT * FROM rides ")
        rows = cls.cur.fetchall()
        rides = []
        for row in rows:
            print(row)
            rides.append({'id': row[0], 'origin': row[1],
                             'destination': row[2], 'date': row[3], "driver": row[4]})
        
        return rides

class Request(Database):
    ''' Defines the Request class'''

    def __init__(self):  
        pass
    @classmethod
    def insert(cls,ride_id, passenger):
        
        query = "INSERT INTO requests (ride_id, passenger) VALUES(%s, %s)"
        cls.cur.execute(query, (ride_id, passenger))

        cls.conn.commit()
        