import xlrd
from collections import OrderedDict
import simplejson as json
import mysql.connector


brackets = '''"'''
delimiter = ";"
source_filename = '../data/Countries_and_ISOs_April_21_2015.xlsx' 


global db_name, tables, syns
db_name = 'ISO_Country'
tables = {}
syns = []
 
tables["country"] = (
    "CREATE  TABLE country ("
    "   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "	name VARCHAR(30),"
    "	iso2 VARCHAR(2),"
    "	iso3 VARCHAR(3),"
    "   code VARCHAR(3),"
    "	status VARCHAR(25)"
    ") ENGINE=InnoDB")

tables["synonyms"] = (
    "CREATE  TABLE synonyms ("
    "   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "	name VARCHAR(30),"
    "   code VARCHAR(3)"
#    "   FOREIGN KEY (ccode)" 
#    "       REFERENCES country(code)"
#    "       ON DELETE CASCADE"
#    "       ON UPDATE CASCADE"
    ") ENGINE=InnoDB")

def get_countries_from_excel():

	wb = xlrd.open_workbook(source_filename)

	sh = wb.sheet_by_index(0)
	countries_list = []
	 
	for rownum in range(1, sh.nrows):
	    c = OrderedDict()
	    row_values = sh.row_values(rownum)
	    c['Name'] = row_values[0]
	    c['ISO2'] = row_values[1]
	    c['ISO3'] = row_values[2]
	    c['Code'] = row_values[3] 
	    c['Status'] = row_values[4]
	    countries_list.append(c)

	return countries_list

def get_synonyms_from_excel():

	wb = xlrd.open_workbook(source_filename)

	sh2 = wb.sheet_by_index(1)

	syns_list = []

	for rownum in range(1, sh2.nrows):
		rvalues = sh2.row_values(rownum)
		value = rvalues[0]
		cset = rvalues[1].split(delimiter)
		for cs in cset:
			syn = OrderedDict()
			syn['Country'] = cs
			syn['Code'] = value
			syns_list.append(syn)
	
	return syns_list

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
            cursor.execute(ddl)
            print "Creating table ", name, "\n"
        except mysql.connector.Error as err:
            success = 0
        else:
            print("OK")
            success = 1
    return success


def insert_country(cursor, c):
    n = c['Name']
    i2 = c['ISO2']
    i3 = c['ISO3']
    co = c['Code']
    st = c['Status']
    add_country = ("INSERT INTO country (name, iso2, iso3, code, status) VALUES (%s, %s, %s, %s, %s)" )
    cursor.execute(add_country, (n, i2, i3, co, st))
    #print add_country
    return

def insert_synonym(cursor, s):
    n = s['Country']
    nc = s['Code']
    add_syn = ("INSERT INTO synonyms (name, code) VALUES (%s, %s)" )
    cursor.execute(add_syn, (n, nc))
    #print add_country
    return

if __name__ == '__main__':

	global conn, cursor
	
	conn = connect()
	cursor = conn.cursor()
	
	create_database(cursor)
	create_tables(cursor)

	clist = get_countries_from_excel()

	syns = get_synonyms_from_excel()

	for ctry in clist:
		insert_country(cursor, ctry)

	for syn in syns:
		insert_synonym(cursor, syn)





