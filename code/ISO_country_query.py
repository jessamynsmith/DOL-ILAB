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
        if conn.is_connected():
            print "Connected to ",db_name.strip()," database on MySQL Server \n"
    except Error as e:
        print(e)
   
    
    return conn

def query(statement):
	result = -1
	cursor.execute(statement)
	results = cursor.fetchall()
	result = str(results[0][0])
	return result

def name_in_db(country_name):
	found = query("SELECT count(1) from country where name = \"{}\"".format(country_name.strip()))
	retval = (True if (int(found) == 1) else False)
	return retval

def iso2_in_db(iso2):
	found = query("SELECT count(1) from country where iso2 = \"{}\"".format(iso2.strip()))
	retval = (True if (int(found) == 1) else False)
	return retval	

def run_syns_aware_query(country_name, querystat, result):
	answer = -1 
	if name_in_db(country_name):
		answer = query(querystat)
	else:
		if is_synonym(country_name):
			iso2 = get_iso2_from_synonyms(country_name)
			if iso2_in_db(iso2):
				if (result == "code"):
					answer = get_code_from_iso2(iso2)
				if (result == "iso2"):
					answer = iso2
				if (result == "iso3"):
					answer = get_iso3_from_iso2(iso2)
				if (result == "status"):
					answer = get_status_from_iso2(iso2)
			else:
				answer = -1
		else:
			answer = -1
	return answer

def get_code_from_name(country_name):
	code = run_syns_aware_query(country_name, "SELECT code FROM country WHERE name = \"{}\"".format(country_name.strip()), "code" )
	return code

def get_iso2_from_name(country_name):
	iso2 = run_syns_aware_query(country_name, "SELECT iso2 FROM country WHERE name = \"{}\"".format(country_name.strip()), "iso2")
	return iso2

def get_iso3_from_name(country_name):
	iso3 = run_syns_aware_query(country_name, "SELECT iso3 FROM country WHERE name = \"{}\"".format(country_name.strip()), "iso3")
	return iso3

def get_status_from_name(country_name):
	status = run_syns_aware_query(country_name, "SELECT status FROM country WHERE name = \"{}\"".format(country_name.strip()), "status")
	return status 

def get_row_from_name(country_name):
	row = []

	if name_in_db(country_name):
		query = ("SELECT name, iso2, iso3, code, status FROM country WHERE name = \"{}\"".format(country_name.strip()))
		cursor.execute(query)
		results = cursor.fetchall()
		row = results[0]
	else:
		if is_synonym(country_name):
			iso2 = get_iso2_from_synonyms(country_name)
			if iso2_in_db(iso2):
				row = get_row_from_iso2(iso2)
			else:
				row = []
		else:
			row = []

	return row 

def get_name_from_iso2(iso2):
	name = query("SELECT name FROM country WHERE iso2 = \"{}\"".format(iso2.strip()))
	return name

def get_code_from_iso2(iso2):
	iso2 = query("SELECT code FROM country WHERE iso2 = \"{}\"".format(iso2.strip()))
	return iso2

def get_iso3_from_iso2(iso2):
	iso3 = query("SELECT iso3 FROM country WHERE iso2 = \"{}\"".format(iso2.strip()))
	return iso3

def get_status_from_iso2(iso2):
	status = query("SELECT status FROM country WHERE iso2 = \"{}\"".format(iso2.strip()))
	return status 

def get_row_from_iso2(iso2):
	row = []

	if iso2_in_db(iso2):
		query = ("SELECT name, iso2, iso3, code, status FROM country WHERE iso2 = \"{}\"".format(iso2.strip()))
		cursor.execute(query)
		results = cursor.fetchall()
		row = results[0]
	else:
		row = []

	return row 

def is_synonym(name):
	found = query("SELECT count(1) FROM synonyms WHERE name = \"{}\"".format(name.strip()))
	retval = (True if (int(found) == 1) else False)
	return retval	

def get_iso2_from_synonyms(name):
	iso2 = query("SELECT iso2 FROM synonyms WHERE name = \"{}\"".format(name.strip()))	
	return iso2

def get_all_countries():
	query = ("SELECT name, iso2, iso3, code, status FROM country")
	cursor.execute(query)
	results = cursor.fetchall()
	return results

def get_all_synonyms():
	query = ("SELECT name, iso2 FROM synonyms")
	cursor.execute(query)
	results = cursor.fetchall()
	return results

def disconnect():
    conn.close()
    print "\n Closed connection to ",db_name.strip()," database on MySQL Server \n"
    return


if __name__ == '__main__':

	conn  = connect()
	cursor = conn.cursor()



	disconnect()


