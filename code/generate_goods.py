

import xlrd
from collections import OrderedDict
import simplejson as json
#from sys import argv
from generate_products import get_countries
 
source_filename = '../source_data/goods.xls' 
xml_header = """<?xml version="1.0" encoding="UTF-8"?>"""


def from_excelsheet(sheetno):
	# Open the workbook and select the first worksheet
	wb = xlrd.open_workbook(source_filename)
	sh = wb.sheet_by_index(sheetno)
	goods_list = []
	# Iterate through each row in worksheet 
	for rownum in range(1, sh.nrows):
	    good = OrderedDict()
	    row_values = sh.row_values(rownum)
	    good['Year'] = int(row_values[0])
	    good['Country'] = str(row_values[1]).strip()
	    good['Good'] = str(row_values[2]).strip()
	    good['Child Labor'] = str(row_values[3]).strip()
	    good['Forced Labor'] = str(row_values[4]).strip()
	    goods_list.append(good)
	return goods_list

def get_goods(goods_list):
	goods = []
	for n in range(0, len(goods_list)):
		go = goods_list[n]['Good'].strip()
		if (go not in goods):
			goods.append(go)
	return goods

def get_good_tuples_for_country(goods_list, country, yr):
	good_tuples = []
	country = country.strip()
	yr = int(yr)
	for num in range(0, len(goods_list)):
		good_tuple = OrderedDict()
		y = int(goods_list[num]['Year'])
		c = goods_list[num]['Country'].strip()
		if (y == yr) and (c == country):
			good_tuple['Good'] = str(goods_list[num]['Good']).strip()
			good_tuple['Child Labor'] = str(goods_list[num]['Child Labor']).strip()
			good_tuple['Forced Labor'] = str(goods_list[num]['Forced Labor']).strip()
			good_tuples.append(good_tuple)
	return good_tuples	

def get_country_tuples_for_good(goods_list,good, yr):
	countries = []
	good = good.strip()
	yr = int(yr)
	for num in range(0, len(goods_list)):
		country_tuple = OrderedDict()
		r = goods_list[num]
		y = int(r['Year'])
		g = str(r['Good']).strip()
		if (y == yr) and ( good.upper() == g.upper()):
			country_tuple['Country'] = str(r['Country']).strip()
			country_tuple['Child Labor'] = str(r['Child Labor']).strip()
			country_tuple['Forced Labor'] = str(r['Forced Labor']).strip()
			countries.append(country_tuple)
	return countries

def raw_dump_to_json(goods_list, fname):
	# Serialize the list of dicts to JSON
	j = json.dumps(goods_list) 
	# Write to file
	with open(fname, 'w') as f:
	    f.write(j)


def to_xml_by_country(goods_list, filename):
	
	target = open(filename, 'w+')

	# Write XML Header
	target.write(xml_header+"\n")
	target.write("<Goods_List>\n")

	# Sets of attributes
	yr = []
	countries = []

	# Group by Country
	for n in range(0, len(goods_list)):
		row = goods_list[n]
		year = int(row['Year'])
		country = str(row['Country']).strip()
		good = str(row['Good']).strip()
		if (year not in yr):
			if (len(yr) > 0) and (n != (len(goods_list))):
				target.write("\t</Year>\n")
				countries = []
			target.write("\t"+"<Year>"+"\n"+"\t\t<Year_Name>"+str(year)+"</Year_Name>"+"\n")
			yr.append(year)
		if 	(country not in countries):
			target.write("\t\t<Country>\n"+"\t\t\t<Country_Name>"+country+"</Country_Name>"+"\n")
			good_tuples = get_good_tuples_for_country(goods_list,country, year)
			target.write("\t\t\t<Goods>\n")
			#print ("Year: " + str(year)+ ": "+country+": "+str(good_tuples))
			for c in range(0, len(good_tuples)):
				#print good_tuples
				target.write("\t\t\t\t<Good>\n")
				target.write("\t\t\t\t\t\t"+"<Good_Name>"+str(good_tuples[c]['Good'])+"</Good_Name>\n")
				target.write("\t\t\t\t\t\t"+"<Child_Labor>"+str(good_tuples[c]['Child Labor'])+"</Child_Labor>\n")
				target.write("\t\t\t\t\t\t"+"<Forced_Labor>"+str(good_tuples[c]['Forced Labor'])+"</Forced_Labor>\n")
				target.write("\t\t\t\t</Good>\n")
			target.write("\t\t\t</Goods>\n")
			target.write("\t\t</Country>\n")
			countries.append(country)
	target.write("\t</Year>\n")
	target.write("</Good_List>\n")
	target.close()
	#print "Closed file"

def to_xml_by_good(goods_list, filename):
	
	target = open(filename, 'w+')

	# Write XML Header
	target.write(xml_header+"\n")
	target.write("<Good_List>\n")
	#print ("written to file")

	# Sets of attributes
	yr = []
	products = []

	# Group by Good
	for n in range(0, len(goods_list)):
		row = goods_list[n]
		year = int(row['Year'])
		country = str(row['Country']).strip()
		good = str(row['Good']).strip()
		if (year not in yr):
			if (len(yr) > 0) and (n != (len(goods_list))):
				target.write("\t</Year>\n")
				products = []
			target.write("\t"+"<Year>"+"\n"+"\t\t<Year_Name>"+str(year)+"</Year_Name>"+"\n")
			yr.append(year)
		if 	(good not in products):
			target.write("\t\t\t<Good>\n"+"\t\t\t\t<Good_Name>"+good+"</Good_Name>"+"\n")
			countryset = get_country_tuples_for_good(goods_list,good, year)
			#print (good+": "+str(countryset))
			target.write("\t\t\t\t\t<Countries>\n")
			for count in range(0, len(countryset)):
				target.write("\t\t\t\t\t\t<Country>\n")
				target.write("\t\t\t\t\t\t\t"+"<Country_Name>"+str(countryset[count]['Country'])+"</Country_Name>\n")
				target.write("\t\t\t\t\t\t\t"+"<Child_Labor>"+str(countryset[count]['Child Labor'])+"</Child_Labor>\n")
				target.write("\t\t\t\t\t\t\t"+"<Forced_Labor>"+str(countryset[count]['Forced Labor'])+"</Forced_Labor>\n")
				target.write("\t\t\t\t\t\t</Country>\n")
			target.write("\t\t\t\t\t</Countries>\n")
			target.write("\t\t\t</Good>\n")
			products.append(good)
	target.write("\t</Year>\n")
	target.write("</Good_List>\n")
	target.close()
	#print "Closed file"

if __name__ == '__main__':
	glist = from_excelsheet(0)
	to_xml_by_country(glist, "../output/goods_2013_by_country.xml")
	to_xml_by_good(glist,"../output/goods_2013_by_good.xml")

	glist = from_excelsheet(1)
	to_xml_by_country(glist, "../output/goods_2012_by_country.xml")
	to_xml_by_good(glist,"../output/goods_2012_by_good.xml")

	glist = from_excelsheet(2)
	to_xml_by_country(glist, "../output/goods_2011_by_country.xml")
	to_xml_by_good(glist,"../output/goods_2011_by_good.xml")

	glist = from_excelsheet(3)
	to_xml_by_country(glist, "../output/goods_2010_by_country.xml")
	to_xml_by_good(glist,"../output/goods_2010_by_good.xml")

	glist = from_excelsheet(4)
	to_xml_by_country(glist, "../output/goods_2009_by_country.xml")
	to_xml_by_good(glist,"../output/goods_2009_by_good.xml")