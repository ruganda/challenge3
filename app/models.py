import os
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import psycopg2


    

class Database():
    """This class does all database related staff"""
        
   
    
    def __init__(self, db = 'ride_db',
                user = os.getenv('USER'),host= os.getenv('HOST'),
                password = os.getenv('PASS'),port = os.getenv('PORT')):
       
        self.conn = psycopg2.connect("dbname='{}' user={} host = {} password={} port={}"
                                    .format(db,user,host,password,port))
        self.cur = self.conn.cursor()
        # self.cur.autocommit = True
        create_table = "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name text, username text, password text, rides_taken INTEGER, rides_given INTEGER )"
        self.cur.execute(create_table)
        create_table2 = "CREATE TABLE IF NOT EXISTS rides (id SERIAL PRIMARY KEY, origin text, destination text, date text, driver text)"
        self.cur.execute(create_table2)
        create_table3 = "CREATE TABLE IF NOT EXISTS requests (id SERIAL PRIMARY KEY, ride_id INTEGER, passenger text)"
        self.cur.execute(create_table3) 

        
  
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

    def get_single_user(self, username):
        try:
            self.cur.execute(
                "SELECT * FROM users WHERE username = '{}'".format(username))
            user = self.cur.fetchone()
            return user
        except:
            return {"error": "Couldn't select"}
    
    def insert_data(self, user):
        """Adds a new record to the database"""
    
        self.cur.execute("INSERT INTO users (name, username, password, rides_taken, rides_given) VALUES( %s, %s, %s,%s,%s)",
                       (user.name, user.username, user.password, self.rides_taken, self.rides_given),)
        self.conn.commit()
    
    
        

    

class Ride(Database):
    '''  Defines a Ride class'''

    def __init__(self,id=None, origin=None, destination=None, date =None):
        ''' Initializes the ride object'''
        self.instance = Database.__init__(self)
        self.id = id
        self.origin = origin
        self.destination = destination
        self.date = date
    

    def find_by_id(self, r_id):
        self.cur.execute(
            "SELECT * FROM rides WHERE id = %(id)s", {'id': r_id})

        row = self.cur.fetchone()
        if row:
            ride = {'id': row[0], 'origin': row[1],
                             'destination': row[2], 'date': row[3], "driver": row[4]}
        self.conn.close()        
        return ride
    
    def insert(self, driver):
        
        query = "INSERT INTO rides (origin, destination, date, driver) VALUES(%s, %s, %s, %s)"
        self.cur.execute(query, (self.origin, self.destination,
                               self.date, driver))
        self.conn.commit()
      

    def fetch_all(self):
        """ Fetches all ride recods from the database"""
        self.cur.execute("SELECT * FROM rides ")
        rows = self.cur.fetchall()
        rides = []
        for row in rows:
            print(row)
            rides.append({'id': row[0], 'origin': row[1],
                             'destination': row[2], 'date': row[3], "driver": row[4]})
        
        return rides

class Request(Database):
    ''' Defines the Request class'''

    def __init__(self):  
        self.instance = Database.__init__(self)
    
    def insert(self,ride_id, passenger):        
        query = "INSERT INTO requests (ride_id, passenger) VALUES('{}', '{}');".format(ride_id, passenger)
        self.cur.execute(query)
        self.conn.commit()
    

    def find_by_id(self, r_id):
        
        
      


        self.cur.execute(
            "SELECT * FROM requests WHERE id = %(id)s", {'id': r_id})
        row = self.cur.fetchone()
        if row:
            request = {'id': row[0], 'origin': row[1],
                             'destination': row[2], 'date': row[3], "driver": row[4]}
               
        return request
    
    def fetch_all(self):
        """ Fetches all request recods from the database"""
        self.cur.execute("SELECT * FROM requests ")
        rows = self.cur.fetchall()
        requests = []
        for row in rows:
            requests.append({'Id':row[0], 'ride': row[1], 'passenger': row[2],})
        return requests

