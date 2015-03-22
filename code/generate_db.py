#!/usr/bin/python

import mysql.connector
import generate_products 
import generate_goods 

db_name = 'DOLILAB'

tables = {}
 
tables['country'] = (
    "CREATE  TABLE country ("
    "   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "   name VARCHAR(45)"
    ") ENGINE=InnoDB")

tables['good'] = (
    "CREATE  TABLE good ("
    "   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "   name VARCHAR(45)"
    ") ENGINE=InnoDB")

tables['product'] = (
    "CREATE  TABLE product ("
    "   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "   name VARCHAR(45)"
    ") ENGINE=InnoDB")  

tables['clflproducts'] = (
    "CREATE  TABLE clflproducts ("
    "   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "   year INT NOT NULL," 
    "   country_id INT NOT NULL,"
    "   product_id INT NOT NULL,"
    "   FOREIGN KEY (country_id)" 
    "       REFERENCES country(id)"
    "       ON DELETE CASCADE"
    "       ON UPDATE CASCADE,"
    "   FOREIGN KEY (product_id)" 
    "       REFERENCES product(id)"
    "       ON DELETE CASCADE"
    "       ON UPDATE CASCADE,"
    ") ENGINE=InnoDB")

tables['clflgoods'] = (
    "CREATE  TABLE clflgoods ("
    "   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "   year INT NOT NULL," 
    "   country_id INT NOT NULL,"
    "   good_id INT NOT NULL,"
    "   child_labor BOOLEAN,"
    "   forced_labor BOOLEAN,"
    "   FOREIGN KEY (country_id)" 
    "       REFERENCES country(id)"
    "       ON DELETE CASCADE"
    "       ON UPDATE CASCADE,"
    "   FOREIGN KEY (good_id)" 
    "       REFERENCES good(id)"
    "       ON DELETE CASCADE"
    "       ON UPDATE CASCADE,"
    ") ENGINE=InnoDB")

def connect():
    # Connect to MySQL database
    try:
        con = mysql.connector.connect(host='localhost', port=8889,
                                       user='root', password='root',
                                       autocommit=True, database=db_name)
        if con.is_connected():
            print "Connected to MySQL Server \n"
    except Error as e:
        print(e)
    
    return con

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
            #cursor.execute("DROP TABLE IF EXISTS {%s}", name) 
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            success = 0
        else:
            print("OK")
            success = 1
    return success

def remove_duplicates(elements):
    output = []
    seen = set()
    for element in elements:
        if element not in seen:
            output.append(element)
            seen.add(element)
    return output

def insert_country(cursor, c):
    add_country = ("INSERT INTO country (name) VALUES (\"{}\")".format(c))
    #print add_country, "\n"
    cursor.execute(add_country)
    return

def insert_good(cursor, g):
    add_good = ("INSERT INTO good (name) VALUES (\"{}\")".format(g))
    cursor.execute(add_good)
    #print add_good, "\n"
    return

def insert_product(cursor, p):
    add_product = ("INSERT INTO product (name) VALUES (\"{}\")".format(p))
    cursor.execute(add_product)
    #print add_product, "\n"
    return

def get_country_id(cursor, country):
    retval  = -1
    query = ("SELECT id FROM country WHERE name = \"{}\"".format(country.strip()))
    cursor.execute(query)
    results = cursor.fetchall()
    if (type(results[0][0]) is int) & (results[0][0] > 0):
        retval = results[0][0]
    return retval

def get_good_id(cursor, good):
    retval = -1
    query = ("SELECT id FROM good WHERE name = \"{}\"".format(good.strip()))
    cursor.execute(query)
    results = cursor.fetchall()
    if (type(results[0][0]) is int) & (results[0][0] > 0):
        retval = results[0][0]
    return retval

def get_product_id(cursor, product):
    retval = -1
    query = ("SELECT id FROM product WHERE name = \"{}\"".format(product.strip()))
    cursor.execute(query)
    results = cursor.fetchall()
    if (type(results[0][0]) is int) & (results[0][0] > 0):
        retval = results[0][0]
    return retval

if __name__ == '__main__':  
    # Build MySQL Infrastructure
    conn = connect()

    cursor = conn.cursor()

    create_database(cursor)
    create_tables(cursor)

    goods_list = generate_goods.get_goods_from_excel()                             # Extract goods from Excel spreadsheet
    goods = sorted(remove_duplicates(generate_goods.get_goods(goods_list)))                # Get list of goods
    gcountries = generate_products.get_countries(goods_list)                          # Get countries mentioned in the list of goods 
    #print "Goods: ", goods, ".\n Length: ", len(goods), "\n"

    products_list = generate_products.get_products_from_excel()                       # Extract products from Excel spreadsheet
    products = sorted(remove_duplicates(generate_products.get_products(products_list)))       # Get list of products
    pcountries = generate_products.get_countries(products_list)                       # Get countries mentioned in the list of products
    #print "Products: ", products, ".\n Length: ", len(products), "\n"

    # Sort countries and remove duplicates
    countries = sorted(remove_duplicates(gcountries + pcountries))
    #print "Countries: ", countries, ".\n Length: ", len(countries), "\n"

    
    for country in countries:
        insert_country(cursor, country)

    for good in goods:
        insert_good(cursor, good)

    for product in products:
        insert_product(cursor, product)

    print get_country_id(cursor, "Nepal")

    conn.close()




