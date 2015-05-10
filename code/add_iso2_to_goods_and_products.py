import json
from collections import OrderedDict
from pprint import pprint
import generate_integrated, generate_goods, generate_products, ISO_country_query, get_region


xml_header = """<?xml version="1.0" encoding="UTF-8"?>"""


def get_ISO2(country):
	conn = ISO_country_query.connect()
	cursor = conn.cursor()
	iso2 = ISO_country_query.get_iso2_from_name(cursor, country)
	ISO_country_query.disconnect(conn)
	return iso2

def list_with_iso2(flist):

	outlist = []

	for fgood in flist:
		good_tuple = OrderedDict()
		good_tuple['Year'] = fgood['Year']
		good_tuple['Country'] = fgood['Country'].strip()
		good_tuple['ISO2'] = get_ISO2(good_tuple['Country'])
		good_tuple['Good'] = fgood['Good']
		good_tuple['Child Labor'] = fgood['Child Labor']
		good_tuple['Forced Labor'] = fgood['Forced Labor']
		good_tuple['Forced Child Labor'] = fgood['Forced Child Labor']
		#print good_tuple
		outlist.append(good_tuple)

	return outlist


def ISO_country_tuples_for_good(goods_list,good, yr):
	countries = []
	good = good.strip()
	yr = int(yr)
	for num in range(0, len(goods_list)):
		country_tuple = OrderedDict()
		r = goods_list[num]
		y = int(r['Year'])
		g = str(r['Good']).strip()
		if (y == yr) and ( good == g):
			country_tuple['Country'] = str(r['Country']).strip()
			country_tuple['ISO2'] = str(r['ISO2']).strip()
			country_tuple['Child Labor'] = str(r['Child Labor']).strip()
			country_tuple['Forced Labor'] = str(r['Forced Labor']).strip()
			country_tuple['Forced Child Labor'] = str(r['Forced Child Labor']).strip()
			countries.append(country_tuple)
	return countries

def to_xml_by_country(goods_list, filename):
	
	target = open(filename, 'w+')

	# Write XML Header
	target.write(xml_header+"\n")
	target.write("<Goods_List>\n")

	# Sets of attributes
	yr = []
	countries = []

	regions = get_region.build()

	# Group by Country
	for n in range(0, len(goods_list)):
		row = goods_list[n]
		year = int(row['Year'])
		country = str(row['Country']).strip()
		iso_2 = str(row['ISO2']).strip()
		region = get_region.find_by_ISO2(iso_2, regions)
		good = str(row['Good']).strip()
		if (year not in yr):
			if (len(yr) > 0) and (n != (len(goods_list))):
				target.write("\t</Year>\n")
				countries = []
			target.write("\t"+"<Year>"+"\n"+"\t\t<Year_Name>"+str(year)+"</Year_Name>"+"\n")
			yr.append(year)
		if 	(country not in countries):
			target.write("\t\t<Country>\n"+"\t\t\t<Country_Name>"+country+"</Country_Name>"+"\n")
			target.write("\t\t\t<ISO2>"+iso_2+"</ISO2>"+"\n")
			target.write("\t\t\t<Region>"+region+"</Region>"+"\n")
			good_tuples = generate_integrated.get_integrated_good_tuples_for_country(goods_list,country, year)
			target.write("\t\t\t<Goods>\n")
			#print ("Year: " + str(year)+ ": "+country+": "+str(good_tuples))
			for c in range(0, len(good_tuples)):
				#print good_tuples
				target.write("\t\t\t\t<Good>\n")
				target.write("\t\t\t\t\t\t"+"<Good_Name>"+str(good_tuples[c]['Good'])+"</Good_Name>\n")
				target.write("\t\t\t\t\t\t"+"<Child_Labor>"+str(good_tuples[c]['Child Labor'])+"</Child_Labor>\n")
				target.write("\t\t\t\t\t\t"+"<Forced_Labor>"+str(good_tuples[c]['Forced Labor'])+"</Forced_Labor>\n")
				target.write("\t\t\t\t\t\t"+"<Forced_Child_Labor>"+str(good_tuples[c]['Forced Child Labor'])+"</Forced_Child_Labor>\n")
				target.write("\t\t\t\t</Good>\n")
			target.write("\t\t\t</Goods>\n")
			target.write("\t\t</Country>\n")
			countries.append(country)
	target.write("\t</Year>\n")
	target.write("</Good_List>\n")
	target.close()

	return

def to_xml_by_good(goods_list, filename):
	
	target = open(filename, 'w+')

	# Write XML Header
	target.write(xml_header+"\n")
	target.write("<Good_List>\n")
	#print ("written to file")

	# Sets of attributes
	yr = []
	products = []

	regions = get_region.build()

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
			countryset = ISO_country_tuples_for_good(goods_list,good, year)
			#print (good+": "+str(countryset))
			target.write("\t\t\t\t\t<Countries>\n")
			for count in range(0, len(countryset)):
				#print countryset[count]
				target.write("\t\t\t\t\t\t<Country>\n")
				target.write("\t\t\t\t\t\t\t"+"<Country_Name>"+str(countryset[count]['Country'])+"</Country_Name>\n")
				iso_2 = str(countryset[count]['ISO2'])
				target.write("\t\t\t\t\t\t\t"+"<ISO2>"+iso_2+"</ISO2>\n")
				region = get_region.find_by_ISO2(iso_2, regions)
				target.write("\t\t\t\t\t\t\t"+"<Region>"+region+"</Region>\n")				
				target.write("\t\t\t\t\t\t\t"+"<Child_Labor>"+str(countryset[count]['Child Labor'])+"</Child_Labor>\n")
				target.write("\t\t\t\t\t\t\t"+"<Forced_Labor>"+str(countryset[count]['Forced Labor'])+"</Forced_Labor>\n")
				target.write("\t\t\t\t\t\t\t"+"<Forced_Child_Labor>"+str(countryset[count]['Forced Child Labor'])+"</Forced_Child_Labor>\n")
				target.write("\t\t\t\t\t\t</Country>\n")
			target.write("\t\t\t\t\t</Countries>\n")
			target.write("\t\t\t</Good>\n")
			products.append(good)
	target.write("\t</Year>\n")
	target.write("</Good_List>\n")
	target.close()

	return

def build():
	glist = generate_goods.from_excelsheet(0)
	plist = generate_products.from_excelsheet(0)
	f_list = generate_integrated.integrate(glist, plist)
	morelist = list_with_iso2(f_list)
	return morelist

def raw_dump_to_json(goods_list, fname):
	# Serialize the list of dicts to JSON
	j = json.dumps(goods_list) 
	# Write to file
	with open(fname, 'w') as f:
	    f.write(j)

if __name__ == '__main__':  
	m = build()
	#print m
	to_xml_by_country(m, "../output/extra/all_goods_with_ISO2_2013_by_country.xml")
	to_xml_by_good(m,"../output/all_goods_with_ISO2_2013_by_good.xml")

	raw_dump_to_json(m, "../output/extra/goods_by_good.json")