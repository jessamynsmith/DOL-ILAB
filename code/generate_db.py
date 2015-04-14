#!/usr/bin/python

import mysql.connector
import generate_products 
import generate_goods 
import generate_master_data

global db_name
db_name = 'DOLILAB'

global tables 
tables = {}
 
tables[0] = (
    "CREATE  TABLE country ("
    "   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "   name VARCHAR(45)"
    ") ENGINE=InnoDB")

tables[1] = (
    "CREATE  TABLE good ("
    "   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "   name VARCHAR(45)"
    ") ENGINE=InnoDB")

tables[2] = (
    "CREATE  TABLE product ("
    "   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "   name VARCHAR(45)"
    ") ENGINE=InnoDB")  

tables[3] = (
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
    "       ON UPDATE CASCADE"
    ") ENGINE=InnoDB")

tables[4] = (
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
    "       ON UPDATE CASCADE"
    ") ENGINE=InnoDB")

tables[5] = (
    "CREATE  TABLE cws ("
    "   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "   country_id INT,"
    "   year VARCHAR(10),"
    "   survey_source VARCHAR(20),"
    "   age_range VARCHAR(6),"
    "   total_child_pop INT,"
    "   total_percentage_working_children FLOAT,"
    "   total_working_population INT,"
    "   cws_agriculture FLOAT,"
    "   cws_services FLOAT,"
    "   cws_industry FLOAT,"
    "   FOREIGN KEY (country_id)" 
    "       REFERENCES country(id)"
    ") ENGINE=InnoDB")

tables[6] = (
    "CREATE  TABLE esas ("
    "   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "   country_id INT,"
    "   year VARCHAR(10)," 
    "   age_range VARCHAR(6),"
    "   percentage FLOAT,"
    "   FOREIGN KEY (country_id)" 
    "       REFERENCES country(id)"
    ") ENGINE=InnoDB")

tables[7] = (
    "CREATE  TABLE cwas ("
    "   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "   country_id INT,"
    "   year VARCHAR(10),"
    "   age_range VARCHAR(6),"
    "   total FLOAT,"
    "   FOREIGN KEY (country_id)" 
    "       REFERENCES country(id)"
    ") ENGINE=InnoDB")

tables[8] = (
    "CREATE  TABLE upcr ("
    "   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "   country_id INT,"
    "   year INT," 
    "   rate FLOAT,"
    "   FOREIGN KEY (country_id)" 
    "       REFERENCES country(id)"
    ") ENGINE=InnoDB")

tables[9] = (
    "CREATE TABLE country_profile ("
    "   year INT NOT NULL," 
    "   country_id INT NOT NULL," 
    "   survey_name VARCHAR(300),"
    "   cws_id INT,"
    "   esas_id INT,"
    "   cwas_id INT,"
    "   upcr_id INT,"
    "   FOREIGN KEY (country_id)"
    "       REFERENCES country(id)"
    "       ON DELETE CASCADE"
    "       ON UPDATE CASCADE,"
    "   FOREIGN KEY (cws_id)"
    "       REFERENCES cws(id)"
    "       ON DELETE CASCADE"
    "       ON UPDATE CASCADE,"
    "   FOREIGN KEY (esas_id)"
    "       REFERENCES esas(id)"
    "       ON DELETE CASCADE"
    "       ON UPDATE CASCADE,"
    "   FOREIGN KEY (cwas_id)"
    "       REFERENCES cwas(id)"
    "       ON DELETE CASCADE"
    "       ON UPDATE CASCADE,"
    "   FOREIGN KEY (upcr_id)" 
    "       REFERENCES upcr(id)"
    "       ON DELETE CASCADE"
    "       ON UPDATE CASCADE,"
    "   CONSTRAINT pk_id_sur PRIMARY KEY (country_id, survey_name)"
    ") ENGINE = InnoDB")

CWS = '''Children's Work Statistics'''
ESAS = "Education Statistics: Attendance Statistics"
CWAS = "Children Working and Studying (7-14 yrs old)"
UPCR = "UNESCO Primary Completion Rate"
empty_brackets = '''""'''
brace = '''"'''

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
    for name, ddl in tables.iteritems():
        try:
            #print("Creating table {}: ".format(name))
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

def insert_clflproduct(cursor, product):
    yr = int(product['Year'])
    cy = product['Country']
    cy_id = int(get_country_id(cursor, cy))
    p = product['Good']
    p_id = int(get_product_id(cursor, p))
  
    add_clflproduct = ("INSERT INTO clflproducts (year, country_id, product_id) VALUES ('%d', '%d', '%d')" % (yr, cy_id, p_id))
    #print add_clflproduct

    cursor.execute(add_clflproduct)
    #print add_clflproduct, "\n"
    return

def insert_clflgood(cursor, good):
    yr = int(good['Year'])
    cy = good['Country']
    cy_id = int(get_country_id(cursor, cy))
    gd = good['Good']
    gd_id = int(get_good_id(cursor, gd))
    cl = (1 if (str(good['Child Labor']).upper() == "T") else 0) 
    fl = (1 if (str(good['Forced Labor']).upper() == "T") else 0)
    add_clflgood = ("INSERT INTO clflgoods (year, country_id, good_id, child_labor, forced_labor) VALUES ('%d', '%d', '%d', '%d', '%d')" % (yr, cy_id, gd_id, cl, fl))

    cursor.execute(add_clflgood)
    #print add_clflgood, "\n"
    return

def empty(x):
    retval = False

    if x == None:
        retval = True

    if (type(x) == type(str())) or (type(x) == type(unicode())): 
        if len(x) == 0:
            retval = True

    return retval

def bracket(x):
    retval = x

    if (type(x)==type(unicode())):
        retval = brace + x + brace

    if (type(x)==type(str())):
        x = str(x).strip()
        if (x[0] == "'") and (x[len(x)-1] == "'"):
            retval = x
        else:
            if (x[0] == '''"''') and (x[len(x)-1] == '''"'''):
                retval = x
            else:
                retval = brace + x + brace
    
    return retval

def insert_master_data(cursor, entry):

        e_year = entry['Year']
        cty = entry['Country']
        cty_id = int(get_country_id(cursor, cty))
        survey_name = (bracket(entry['Survey Name']) if (not empty(entry['Survey Name'])) else empty_brackets)
        cws_year = (bracket(entry[CWS+' : Year']) if (not empty(entry[CWS+' : Year'])) else empty_brackets)
        cws_survey_source = (bracket(entry[CWS+' : Survey Source']) if (not empty(entry[CWS+' : Survey Source'])) else empty_brackets)
        cws_age_range = (bracket(entry[CWS+' : Age Range']) if (not empty(entry[CWS+' : Age Range'])) else empty_brackets)
        cws_tcp = (int(entry[CWS+' : Total Child Population']) if (not empty(entry[CWS+' : Total Child Population'])) else int(0))
        cws_twc = (float(entry[CWS+' : Total % of Working Children']) if (not empty(entry[CWS+' : Total % of Working Children'])) else float(0.0))
        cws_twp = (int(entry[CWS+' : Total Working Population'])  if (not empty(entry[CWS+' : Total Working Population'])) else int(0))
        cws_a = (float(entry[CWS+' : Agriculture']) if (not empty(entry[CWS+' : Agriculture'])) else float(0.0))
        cws_s = (float(entry[CWS+' : Service']) if (not empty(entry[CWS+' : Service'])) else float(0.0))
        cws_i = (float(entry[CWS+' : Industry']) if (not empty(entry[CWS+' : Industry'])) else float(0.0))
        esas_year = (bracket(entry[ESAS+' : Year']) if (not empty(entry[ESAS+' : Year'])) else empty_brackets)
        esas_age_range = (bracket(entry[ESAS+' : Age Range']) if (not empty(entry[ESAS+' : Age Range'])) else empty_brackets)
        esas_p = (float(entry[ESAS+' : %'])  if (not empty(entry[ESAS+' : %'])) else float(0.0))
        cwas_year = (bracket(entry[CWAS+' : Year']) if (not empty(entry[CWAS+' : Year'])) else empty_brackets)
        cwas_age_range = (bracket(entry[CWAS+' : Age Range']) if (not empty(entry[CWAS+' : Age Range'])) else empty_brackets)
        cwas_total = (float(entry[CWAS+' : Total'])  if (not empty(entry[CWAS+' : Total'])) else float(0.0))
        upcr_year = (entry[UPCR+' : Year'] if (not empty(entry[UPCR+' : Year'])) else empty_brackets)
        upcr_rate = (entry[UPCR+' : Rate'] if (not empty(entry[UPCR+' : Rate'])) else empty_brackets) 

        #Insert into CWS     
        add_cws = ("INSERT INTO cws (country_id, year, survey_source, age_range, total_child_pop, total_percentage_working_children, total_working_population, cws_agriculture, cws_services, cws_industry) VALUES (%d, %s, %s, %s, %d, %.1f, %d, %.1f, %.1f, %.1f)") % (cty_id, cws_year, cws_survey_source, cws_age_range, cws_tcp, cws_twc, cws_twp, cws_a, cws_s, cws_i)
        cursor.execute(add_cws)
        cws_id = cursor.lastrowid
    
        #Insert into ESAS
        add_esas = ("INSERT INTO esas (country_id, year, age_range, percentage) VALUES ('%d', '%s', '%s', '%.1f')") % (cty_id, esas_year, esas_age_range, esas_p)
        cursor.execute(add_esas)
        esas_id = cursor.lastrowid

        #Insert into CWAS
        add_cwas = ("INSERT INTO cwas (country_id, year, age_range, total) VALUES (%d, %s, %s, %.1f)") % (cty_id, cwas_year, cwas_age_range, cwas_total)
        cursor.execute(add_cwas)
        cwas_id = cursor.lastrowid
        
        #Insert into UPCR
        add_upcr = ("INSERT INTO upcr (country_id, year, rate) VALUES (%d, %s, %s)") % (cty_id, upcr_year, upcr_rate)
        cursor.execute(add_upcr)
        upcr_id = cursor.lastrowid

        #Insert into country_profile 
        add_country_profile = ("INSERT INTO country_profile (year, country_id, survey_name, cws_id, esas_id, cwas_id, upcr_id) VALUES (%d, %d, %s, %d, %d, %d, %d)") % (e_year, cty_id, survey_name, cws_id, esas_id, cwas_id, upcr_id)
        cursor.execute(add_country_profile)
        
        return



if __name__ == '__main__':  
    # Build MySQL Infrastructure

    global conn
    conn = connect()

    global cursor
    cursor = conn.cursor()

    create_database(cursor)

    create_tables(cursor)

    goods_list = generate_goods.get_goods_from_excel()                             # Extract goods from Excel spreadsheet
    goods = sorted(remove_duplicates(generate_goods.get_goods(goods_list)))                # Get list of goods
    gcountries = generate_products.get_countries(goods_list)                          # Get countries mentioned in the list of goods 
    ##print "Goods: ", goods, ".\n Length: ", len(goods), "\n"

    products_list = generate_products.get_products_from_excel()                       # Extract products from Excel spreadsheet
    products = sorted(remove_duplicates(generate_products.get_products(products_list)))       # Get list of products
    pcountries = generate_products.get_countries(products_list)                       # Get countries mentioned in the list of products
    ##print "Products: ", products, ".\n Length: ", len(products), "\n"

    #Get Master Data
    master_data = generate_master_data.get_master_data_from_excel()
    
    mcountries = generate_products.get_countries(master_data) 

    # Sort countries and remove duplicates
    countries = sorted(remove_duplicates(gcountries + pcountries + mcountries))
    #print "Countries: ", countries, ".\n Length: ", len(countries), "\n"



    # Insert entries into country table
    for country in countries:
        insert_country(cursor, country)

    # Insert entries into good table
    for good in goods:
        insert_good(cursor, good)

    # Insert entries in product table
    for product in products:
        insert_product(cursor, product)

    # Insert entries in clflgood table
    for good in goods_list:
        insert_clflgood(cursor, good)

    # Insert entries in clflproduct table
    for product in products_list:
        insert_clflproduct(cursor, product)

    # Insert entries into master data tables
    for entry in master_data:
        insert_master_data(cursor, entry)



    conn.close()




