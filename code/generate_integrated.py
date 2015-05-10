
import generate_products
import generate_goods
from collections import OrderedDict

open_bracket = "("
slash = "/"
xml_header = """<?xml version="1.0" encoding="UTF-8"?>"""

def canonical_good(name):
	retname = name.strip()

	if name.find(open_bracket) != -1:
		retname = name[:name.find(open_bracket)].strip()
	elif name.find(slash) != -1:
		retname = name[:name.find(slash)].strip()

	return retname

def goods_equal(good1, good2):
	val = (True if (good1.upper() == good2.upper()) else False)
	return val


def countries_equal(c1, c2):
	val = (True if (c1.upper() == c2.upper()) else False)
	return val


def good_found(year, country, good, plist):
	value = False
	g = canonical_good(good)
	c = country
	year = int(year)

	for prod in plist:
		p = canonical_good(prod['Good'])
		y = int(prod['Year'])
		if (countries_equal(c, prod['Country'])) & (goods_equal(g,p)) & (year == y):
			value = True
			break
	return value


def integrate(glist, plist):
	out_list = []

	for good in glist:
		integrated_good = OrderedDict()
		integrated_good = good
		search_good = integrated_good['Good']
		search_country = integrated_good['Country']
		search_year = integrated_good['Year']
		integrated_good['Forced Child Labor'] = ( "T" if (good_found(search_year, search_country, search_good, plist)) else "F")
		out_list.append(integrated_good)

	return out_list


def get_integrated_good_tuples_for_country(goods_list, country, yr):
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
			good_tuple['Forced Child Labor'] = str(goods_list[num]['Forced Child Labor']).strip()
			good_tuples.append(good_tuple)
	return good_tuples


def get_integrated_country_tuples_for_good(goods_list,good, yr):
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
			good_tuples = get_integrated_good_tuples_for_country(goods_list,country, year)
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
			countryset = get_integrated_country_tuples_for_good(goods_list,good, year)
			#print (good+": "+str(countryset))
			target.write("\t\t\t\t\t<Countries>\n")
			for count in range(0, len(countryset)):
				target.write("\t\t\t\t\t\t<Country>\n")
				target.write("\t\t\t\t\t\t\t"+"<Country_Name>"+str(countryset[count]['Country'])+"</Country_Name>\n")
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
	flist = integrate(glist, plist)
	return flist

if __name__ == '__main__':

	full_list = build()

	to_xml_by_country(full_list, "../output/extra/all_goods_2013_by_country.xml")
	to_xml_by_good(full_list,"../output/extra/all_goods_2013_by_good.xml")


	