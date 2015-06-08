import json
import csv
import xlrd
from collections import OrderedDict

# Global XML Header String
xml_header = """<?xml version="1.0" encoding="UTF-8"?>"""

source_filename = "../source_data/RAPP_2013.xlsx"

# Break Characters in a Good Name
open_bracket = "("
slash = "/"
comma = ","
semicolon = ";"
default_error = -1
tab = "\t"
newline = "\n"
encoding_standard = "utf-8"


# Function that returns XML Header
def get_xml_header():
	return xml_header

def get_default_error():
	return default_error

def get_source_filename():
	return source_filename

def get_encoding_standard():
	return encoding_standard

def get_newline():
	return newline

def from_excelsheet(filename, sheetno, startrow, tags):
	wb = xlrd.open_workbook(filename)
	sh = wb.sheet_by_index(sheetno)
	rows = []
	for rownum in range(startrow, sh.nrows):
		row = OrderedDict()
		row_values = sh.row_values(rownum)
		for n in range(0,len(tags)):
			key = tags[n]
			try:
				row[key] = str(row_values[n]).strip()
			except UnicodeEncodeError:
				row[key] = row_values[n].encode(encoding_standard).strip()
		rows.append(row)
	return rows

# Function that return the trimmed version of a good name (before an open bracket or slash)
def canonical_good(name):
	retname = name.strip()
	if name.find(open_bracket) != -1:
		retname = name[:name.find(open_bracket)].strip()
	elif name.find(slash) != -1:
		retname = name[:name.find(slash)].strip()
	return retname

#Function that tests if two good names are equal
def goods_equal(good1, good2):
	val = (True if (good1.upper() == good2.upper()) else False)
	return val

#Function that tests if two country names are equal
def countries_equal(c1, c2):
	val = (True if (c1.upper() == c2.upper()) else False)
	return val

#Function that retrieves data from a json file
def get_json_data(filename):
	data = []
	with open(filename) as json_file:
		data = json.load(json_file)
	return data

#Function that sends data to a json file
def to_json(filename, data):
	j = json.dumps(data) 	
	with open(filename, 'w+') as f:
	    f.write(j)
	return

#Funtion that retrieves data from a CSV file
def get_csv_data(filename):
	data = []
	with open(filename, "rb") as file_obj:
		reader = csv.reader(file_obj)
		for row in reader:
			data.append(" "+row)
	return data

#Function that sends data to a CSV file
def to_csv(filename, data):
	with open(filename, "wb") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		for line in data:
			writer.writerow(line)
	return

def to_csv_from_OD(filename, data):
	csvdata = to_CSV_data(data)
	to_csv(filename, csvdata)
	return

def to_str(val):
	result = default_error
	try:
		result = str(val)
	except UnicodeEncodeError:
		result = val.encode(encoding_standard)
	return result

#Function that converts a generic List of OrderedDicts to a data tuples for a CSV file
def to_CSV_data(ODict):
	data  = []
	firstrow = ""
	for n in range(0, len(ODict)): #Go through the List of OrderedDict
		entry = ODict[n] 
		entry_list = list(entry.items())
		if (n == 0):  #Construct the heading
			for m in range(0,len(entry_list)):
				heading = entry_list[m][0]
				firstrow = firstrow + heading 
				if (m < (len(entry_list) - 1)):
					firstrow = firstrow + comma
			data.append(firstrow.split(comma))
		row = ""
		for m in range(0,len(entry_list)): 
			value = ""
			value = to_str(entry_list[m][1])
			row = row + value
			if (m < (len(entry_list)-1)):
				row = row + semicolon
		data.append(row.split(semicolon))
	return data

def to_list(initialstr, delimiter, tag):
	result = default_error
	temp = initialstr.split(delimiter)
	arr = []
	for t in temp:
		b = OrderedDict()
		b[tag] = t
		arr.append(b)
	if (len(arr) > 0):
		result = arr
	return result

def count(list, tag):
	resl = []
	for entry in list:
		resl.append(entry[tag])
	result = len(set(resl))
	print "for ", tag," the count is ", result
	return result

def get_json_data(c_json_file):
	country_data = []
	with open(c_json_file) as json_file:
		country_data = json.load(json_file)
	return country_data


def get_tuple_by_X(cname, tag, list):

	result = OrderedDict()
	fixed = str(cname).strip().upper()

	for entry in list:
		sname = str(entry[tag]).strip().upper()
		if (sname == fixed):
			mks = entry.keys()
			newrow = OrderedDict()
			for n in range(0,len(mks)):
				currentkey = mks[n]
				newrow[currentkey] = entry[currentkey]
			result = newrow
			break

	return result


def create_starting_xml_tag(keyn):
	result = ""
	retk = to_str(keyn)
	result = "<" +keyn +">"
	return result

def create_closing_xml_tag(keyn):
	result = ""
	retk = to_str(keyn)
	result = "</" +keyn +">"
	return result

def tabs(no):
	return (tab * no)

def write_record(target, cr, count):
	ckeys = cr.keys()
	for n in range(0, len(cr)): 
		kv = cr[ckeys[n]]
		if (type(kv) == list):
			target.write( tabs(count) + create_starting_xml_tag(ckeys[n]) + newline)
			count += 1
			for l in kv:
				this_key_group = (ckeys[n])[:(len(ckeys[n])-1)]
				if len(kv) > 0:
					if ckeys[n].strip().upper() == "COUNTRIES":
						this_key_group = "Country"
					target.write( tabs(count) + create_starting_xml_tag(this_key_group) + newline)
				write_record(target, l, count+1)
				if len(kv) > 0:
					target.write( tabs(count) + create_closing_xml_tag(this_key_group) + newline)
			end = create_closing_xml_tag(ckeys[n]) + newline
			target.write( tabs(count) + end )
		else:
			keyname = to_str(ckeys[n])
			start = create_starting_xml_tag(keyname)
			val = to_str(cr[keyname])
			end = create_closing_xml_tag(keyname)
			target.write( tabs(count) + start + val + end + newline )
	return
