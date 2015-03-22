

import xlrd
from collections import OrderedDict
import simplejson as json
#from sys import argv
 
source_filename = '../source_data/products.xls' 
xml_header = """<?xml version="1.0" encoding="UTF-8"?>"""

def get_countries(goods_list):
	countries = []
	for n in range(0, len(goods_list)):
		co = goods_list[n]['Country'].strip()
		if (co not in countries):
			countries.append(co)
	return countries

def get_products(goods_list):
	goods = []
	for n in range(0, len(goods_list)):
		go = goods_list[n]['Good'].strip()
		if (go not in goods):
			goods.append(go)
	return goods

def get_goods_for_country(goods_list,country, yr):
	products = []
	for num in range(0, len(goods_list)):
		r = goods_list[num]
		y = int(r['Year'])
		c = str(r['Country']).strip()
		g = str(r['Good']).strip()
		if (y == yr) and ( c == country):
			products.append(g)
	return products

def get_countries_for_good(goods_list,good, yr):
	countries = []
	for num in range(0, len(goods_list)):
		r = goods_list[num]
		y = int(r['Year'])
		c = str(r['Country']).strip()
		g = str(r['Good']).strip()
		if (y == yr) and ( good == g):
			countries.append(c)
	return countries

def get_products_from_excel():
	# Open the workbook and select the first worksheet
	wb = xlrd.open_workbook(source_filename)
	sh = wb.sheet_by_index(0)
	goods_list = []
	# Iterate through each row in worksheet 
	for rownum in range(1, sh.nrows):
	    good = OrderedDict()
	    row_values = sh.row_values(rownum)
	    good['Year'] = int(row_values[0])
	    good['Country'] = str(row_values[1]).strip()
	    good['Good'] = str(row_values[2]).strip()
	    goods_list.append(good)
	return goods_list

def raw_dump_to_json(goods_list, filename):
	# Serialize the list of dicts to JSON
	j = json.dumps(goods_list) 
	# Write to file
	with open(filename, 'w') as f:
	    f.write(j)


def xml_products_by_country(goods_list, filename):
	
	target = open(filename, 'w+')

	# Write XML Header
	target.write(xml_header+"\n")
	target.write("<Product List>\n")
	#print ("written to file")

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
			goodset = get_goods_for_country(goods_list,country, year)
			#print (country+": "+str(goodset))
			target.write("\t\t\t<Product>\n")
			for count in range(0, len(goodset)):
				target.write("\t\t\t\t"+"<Product_Name>"+goodset[count]+"</Product_Name>\n")
			target.write("\t\t\t</Product>\n")
			target.write("\t\t</Country>\n")
			countries.append(country)
	target.write("\t</Year>\n")
	target.write("</Product List>\n")
	target.close()
	#print "Closed file"

def xml_products_by_product(goods_list, filename):
	
	target = open(filename, 'w')
	# Wipe the file
	target.truncate()

	# Write XML Header
	target.write(xml_header+"\n")
	target.write("<Product List>\n")
	#print ("written to file")

	# Sets of attributes
	yr = []
	products = []

	# Group by Country
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
			target.write("\t\t<Product>\n"+"\t\t\t<Product_Name>"+good+"</Product_Name>"+"\n")
			countryset = get_countries_for_good(goods_list,good, year)
			#print (good+": "+str(countryset))
			target.write("\t\t\t<Countries>\n")
			for count in range(0, len(countryset)):
				target.write("\t\t\t\t"+"<Country_Name>"+countryset[count]+"</Country_Name>\n")
			target.write("\t\t\t</Countries>\n")
			target.write("\t\t</Product>\n")
			products.append(good)
	target.write("\t</Year>\n")
	target.write("</Product List>\n")
	target.close()
	#print "Closed file"

if __name__ == '__main__':
	plist = get_products_from_excel()
	xml_products_by_country(plist, "../output/products_by_country.xml")
	xml_products_by_product(plist, "../output/products_by_product.xml")

