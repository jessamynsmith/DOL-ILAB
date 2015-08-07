import utility
import mysql.connector
from collections import OrderedDict

brackets = '''"'''
delimiter = ";"

source_filename = '../source_data/ISO_Countries/Countries_and_ISOs_April_21_2015.xlsx' 
json_target = "../output/ISO_Countries/ISO_Countries.json"
syn_json_target = ".../output/ISO_Countries/ISO_Country_Synonyms.json"
csv_target = "../output/ISO_Countries/ISO_Countries.csv"
syn_csv_target = "../output/ISO_Countries/ISO_Country_Synonyms.csv"

global db_name, tables, syns
db_name = 'ISO_Country'
tables = {}
syns = []

iso_country_mappings = ["Name", "ISO2", "ISO3", "Code", "Status"]
synonym_mappings = [ "ISO2", "ISO3", "Country"]


tables["country"] = (
    "CREATE  TABLE country ("
    "   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "	name VARCHAR(100),"
    "	iso2 VARCHAR(2),"
    "	iso3 VARCHAR(3),"
    "   code VARCHAR(3),"
    "	status VARCHAR(25)"
    ") ENGINE=InnoDB")

tables["synonyms"] = (
    "CREATE  TABLE synonyms ("
    "   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "	name VARCHAR(100),"
    "   iso2 VARCHAR(2),"
    "   iso3 VARCHAR(3)"
    ") ENGINE=InnoDB")


def get_ISO_countries():
    result = utility.from_excelsheet(source_filename, 0, 1, iso_country_mappings)
    return result

def get_synonyms():
    result = utility.from_excelsheet(source_filename, 1, 1, synonym_mappings)
    return result

def build():
    ret = []
    cs = get_ISO_countries()
    ss = get_synonyms()
    ret.append(cs)
    ret.append(ss)
    return ret

def ISO2_from_name(cname, cslist):
    res = utility.get_default_error()
    iso2 = ISO_from_name(cname, cslist, "ISO2")
    if iso2 != utility.get_default_error():
        res = iso2
    return res 

def ISO3_from_name(cname, cslist):
    result = utility.get_default_error()
    iso3 = ISO_from_name(cname, cslist, "ISO3")
    if iso3 != utility.get_default_error():
        result = iso3
    return result

def ISO3_from_ISO2(iso2, cslist):
    result = utility.get_default_error()
    cs = cslist[0]
    for row in cs:
        if str(row["ISO2"]) == str(iso2):
            result = row["ISO3"]
    return result

def ISO_from_name(cname, cslist, tag):
    res = utility.get_default_error()
    found = False
    cs = cslist[0]
    ss = cslist[1]
    sname = (utility.to_str(cname)).upper().strip()

    for c in cs:
        name = (utility.to_str(c['Name'])).upper().strip()
        if (sname == name):
            found = True
            res = c[tag]
            break
        else:
            found = False

    if (not found):
        for s in ss:
            names = ((utility.to_str(s['Country'])).upper().strip()).split(delimiter)
            for name in names:
                mname = str(name).upper().strip()
                if (sname == mname):
                    res = s[tag]
                    found = True
                    #print "MINOR CONCERN - ", sname, " was found in the country synonym list."
                    break
            if found == True:
                break

    if res == utility.get_default_error(): 
        print "MAJOR ERROR - ", sname, " was not found in the ISO country or synonym lists"

    return res 

def name_from_ISO3(iso3, cslist):
    result = utility.get_default_error()
    cs = cslist[0]
    for row in cs:
        if str(row["ISO3"]) == str(iso3):
            result = row["Name"]
    return result


def connect():
    Error  = ""
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
    try:
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
    return

def create_tables(cursor):
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
    return

def insert_synonym(cursor, s):
    n = s['Country']
    nc = s['ISO2']
    nca = s['ISO3']
    add_syn = ("INSERT INTO synonyms (name, iso2, iso3) VALUES (%s, %s, %s)" )
    cursor.execute(add_syn, (n, nc, nca))
    return

# Creates a JSON file for the data
def to_json(filename, data):
    utility.to_json(filename, data)
    return

# Creates a CSV file for the data
def to_csv(filename, data):
    utility.to_csv_from_OD(filename, csvdata)
    return

def expand_syns(syns):
    result = utility.get_default_error()
    working_array = []
    for s in syns:
        b = OrderedDict()
        b['ISO2'] = s['ISO2']
        b['ISO3'] = s['ISO3']
        strg = s['Country']
        b['Country'] = utility.to_list(strg,";","name")
        working_array.append(b)
    result = working_array
    return result

if __name__ == '__main__':

    countries = build()

    print ISO3_from_name("Jamaica", countries)

    for d in countries[1]:
        print d['Country'].split(delimiter)