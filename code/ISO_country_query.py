import generate_ISO_country
import mysql.connector

global db_name, conn, cursor
db_name = 'ISO_Country'

def connect():
    Error  = ""
    # Connect to MySQL database
    try:
        conn = mysql.connector.connect(host='localhost', port=8889,
                                       user='root', password='root',
                                       autocommit=True, database=db_name)
        #if conn.is_connected():
        #	print Connected to ",db_name.strip()," database on MySQL Server \n"
    except Error as e:
        print(e)
   
    
    return conn

def query(cursor, statement):
	result = -1
	cursor.execute(statement)
	results = cursor.fetchall()
	result = str(results[0][0])
	return result

def name_in_db(cursor, country_name):
	found = query(cursor, "SELECT count(1) from country where name = \"{}\"".format(country_name.strip()))
	retval = (True if (int(found) == 1) else False)
	return retval

def iso2_in_db(cursor, iso2):
	found = query(cursor, "SELECT count(1) from country where iso2 = \"{}\"".format(iso2.strip()))
	retval = (True if (int(found) == 1) else False)
	return retval	

def run_syns_aware_query(cursor, country_name, querystat, result):
	answer = -1 
	if name_in_db(cursor, country_name):
		answer = query(cursor, querystat)
	else:
		if is_synonym(cursor, country_name):
			iso2 = get_iso2_from_synonyms(cursor, country_name)
			if iso2_in_db(cursor, iso2):
				if (result == "code"):
					answer = get_code_from_iso2(cursor, iso2)
				if (result == "iso2"):
					answer = iso2
				if (result == "iso3"):
					answer = get_iso3_from_iso2(cursor, iso2)
				if (result == "status"):
					answer = get_status_from_iso2(cursor, iso2)
			else:
				answer = -1
		else:
			answer = -1
	return answer

def get_code_from_name(cursor, country_name):
	code = run_syns_aware_query(cursor, country_name, "SELECT code FROM country WHERE name = \"{}\"".format(country_name.strip()), "code" )
	return code

def get_iso2_from_name(cursor, country_name):
	iso2 = run_syns_aware_query(cursor, country_name, "SELECT iso2 FROM country WHERE name = \"{}\"".format(country_name.strip()), "iso2")
	return iso2

def get_iso3_from_name(cursor, country_name):
	iso3 = run_syns_aware_query(cursor, country_name, "SELECT iso3 FROM country WHERE name = \"{}\"".format(country_name.strip()), "iso3")
	return iso3

def get_status_from_name(cursor, country_name):
	status = run_syns_aware_query(cursor, country_name, "SELECT status FROM country WHERE name = \"{}\"".format(country_name.strip()), "status")
	return status 

def get_row_from_name(cursor, country_name):
	row = []

	if name_in_db(cursor, country_name):
		q = ("SELECT name, iso2, iso3, code, status FROM country WHERE name = \"{}\"".format(country_name.strip()))
		cursor.execute(q)
		results = cursor.fetchall()
		row = results[0]
	else:
		if is_synonym(cursor, country_name):
			iso2 = get_iso2_from_synonyms(cursor, country_name)
			if iso2_in_db(cursor, iso2):
				row = get_row_from_iso2(cursor, iso2)
			else:
				row = []
		else:
			row = []

	return row 

def get_name_from_iso2(cursor, iso2):
	name = query(cursor, "SELECT name FROM country WHERE iso2 = \"{}\"".format(iso2.strip()))
	return name

def get_code_from_iso2(cursor, iso2):
	iso2 = query(cursor, "SELECT code FROM country WHERE iso2 = \"{}\"".format(iso2.strip()))
	return iso2

def get_iso3_from_iso2(cursor, iso2):
	iso3 = query(cursor, "SELECT iso3 FROM country WHERE iso2 = \"{}\"".format(iso2.strip()))
	return iso3

def get_status_from_iso2(cursor, iso2):
	status = query(cursor, "SELECT status FROM country WHERE iso2 = \"{}\"".format(iso2.strip()))
	return status 

def get_row_from_iso2(cursor, iso2):
	row = []

	if iso2_in_db(iso2):
		q = ("SELECT name, iso2, iso3, code, status FROM country WHERE iso2 = \"{}\"".format(iso2.strip()))
		cursor.execute(q)
		results = cursor.fetchall()
		row = results[0]
	else:
		row = []

	return row 

def is_synonym(cursor, name):
	found = query(cursor, "SELECT count(1) FROM synonyms WHERE name = \"{}\"".format(name.strip()))
	retval = (True if (int(found) == 1) else False)
	return retval	

def get_iso2_from_synonyms(cursor, name):
	iso2 = query(cursor, "SELECT iso2 FROM synonyms WHERE name = \"{}\"".format(name.strip()))	
	return iso2

def get_all_countries(cursor):
	q = ("SELECT name, iso2, iso3, code, status FROM country")
	cursor.execute(q)
	results = cursor.fetchall()
	return results

def get_all_synonyms(cursor):
	q = ("SELECT name, iso2 FROM synonyms")
	cursor.execute(q)
	results = cursor.fetchall()
	return results

def disconnect(conn):
    conn.close()
    #print "\n Closed connection to ",db_name.strip()," database on MySQL Server \n"
    return


if __name__ == '__main__':

	conn  = connect()
	cursor = conn.cursor()



	disconnect()


