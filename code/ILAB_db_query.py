import mysql.connector

global db_name, encoding_standard
db_name = 'DOLILAB'
encoding_standard = "utf-8"

def connect():
    Error  = ""
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

def get_country_id(cursor, country):
    retval  = -1
    query = ("SELECT id FROM country WHERE name = \"{}\"".format(str(country)))
    cursor.execute(query)
    results = cursor.fetchall()
    if (type(results[0][0]) is int) & (results[0][0] > 0):
        retval = results[0][0]
    return retval

def get_countries(cursor):
    retval  = -1
    query = ("SELECT name FROM country")
    cursor.execute(query)
    results = cursor.fetchall()
    if len(results) > 0:
    	retval = []
    	for c in results:
    		retval.append(c[0].encode(encoding_standard))
    return retval

def get_good_id(cursor, good):
    retval  = -1
    query = ("SELECT id FROM good WHERE name = \"{}\"".format(good.strip()))
    cursor.execute(query)
    results = cursor.fetchall()
    if (type(results[0][0]) is int) & (results[0][0] > 0):
        retval = results[0][0]
    return retval

def get_goods(cursor):
    retval  = -1
    query = ("SELECT name FROM good")
    cursor.execute(query)
    results = cursor.fetchall()
    if len(results) > 0:
    	retval = []
    	for c in results:
    		retval.append(c[0].encode(encoding_standard))
    return retval

def get_product_id(cursor, good):
    retval  = -1
    query = ("SELECT id FROM product WHERE name = \"{}\"".format(good.strip()))
    cursor.execute(query)
    results = cursor.fetchall()
    if (type(results[0][0]) is int) & (results[0][0] > 0):
        retval = results[0][0]
    return retval

def get_products(cursor):
    retval  = -1
    query = ("SELECT name FROM product")
    cursor.execute(query)
    results = cursor.fetchall()
    if len(results) > 0:
    	retval = []
    	for c in results:
    		retval.append(c[0].encode(encoding_standard))
    return retval


if __name__ == '__main__':  

    global conn
    conn = connect()

    cursor = conn.cursor()

    at = get_products(cursor)
    
    #print at	
    for net in at:
    	print get_product_id(cursor, net), ": ", net 

