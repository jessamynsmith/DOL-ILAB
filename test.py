#!/usr/bin/python

import mysql.connector

db_name = 'DOLILAB'

tables = {}
 
tables['country'] = (
    "CREATE  TABLE 'good' ("
    "   'id' INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "   'name' VARCHAR(45)"
    ") ENGINE=InnoDB")

tables['good'] = (
    "CREATE  TABLE 'good' ("
    "   'id' INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "   'name' VARCHAR(45),"
    "   'description' VARCHAR(200)"
    ") ENGINE=InnoDB")

tables['product'] = (
    "CREATE  TABLE 'product' ("
    "   'id' INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "   'name' VARCHAR(45),"
    "   'description' VARCHAR(200)"
    ") ENGINE=InnoDB")  

tables['clflgoods'] = (
    "CREATE  TABLE 'clflgoods' ("
    "   'id' INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "   'year' INT NOT NULL," 
    "   'country_id' INT NOT NULL,"
    "   'good_id' INT NOT NULL,"
    "   'child_labor' BOOLEAN,"
    "   'forced_labor' BOOLEAN,"
    "   CONSTRAINT 'fk_country'"
    "       FOREIGN KEY ('country_id') REFERENCES 'country' ('id')"
    "   CONSTRAINT 'fk_good'"
    "       FOREIGN KEY ('good_id') REFERENCES 'good' ('id')"
    ") ENGINE=InnoDB")

tables['clflproducts'] = (
    "CREATE  TABLE 'clflproducts' ("
    "   'id' INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "   'year' INT NOT NULL," 
    "   'country_id' INT NOT NULL,"
    "   'product_id' INT NOT NULL,"
    "   CONSTRAINT 'fk_country'"
    "       FOREIGN KEY ('country_id') REFERENCES 'country' ('id')"
    "   CONSTRAINT 'fk_good'"
    "       FOREIGN KEY ('product_id') REFERENCES 'product' ('id')"
    ") ENGINE=InnoDB")

def connect():
    # Connect to MySQL database
    try:
        conn = mysql.connector.connect(host='localhost', port=8889,
                                       user='root', password='root')
        if conn.is_connected():
            print('Connected to MySQL Server')
            pointer = conn.cursor()
    except Error as e:
        print(e)
    return conn

def create_database(cursor):
    # Creating ILAB Database
    try:
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
    return

def create_tables(cursor):
    # Creating tables in ILAB Database 
    success = 0
    for name, ddl in tables.iteritems():
        try:
            print("Creating table {}: ".format(name))
            cursor.execute("DROP TABLE IF EXISTS {%s}", name) 
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            success = 0
        else:
            print("OK")
            success = 1
    return success

def initialize_database():
    # Initialize the ILAB Database and Tables 
    connection = connect()
    cur = connection.cursor()
    create_database(cur)
    create_tables(cur)
    return cur

if __name__ == '__main__':
    cursor = initialize_database()




'''
hire_start = datetime.date(1999, 1, 1)
hire_end = datetime.date(1999, 12, 31)

cursor.execute(query, (hire_start, hire_end))

for (first_name, last_name, hire_date) in cursor:
  print("{}, {} was hired on {:%d %b %Y}".format(
    last_name, first_name, hire_date))

cursor.close()
cnx.close() 
'''

