

import utility
import ISO_countries 
import sectors 
import regions 
import special_chars
from collections import OrderedDict

csv_2013_target = '../output/2013/extra/goods_from_XL.csv' 
xml_2013_target_by_country = '../output/2013/extra/goods_by_country_from_XL.xml' 
xml_2013_target_by_good = '../output/2013/extra/goods_by_good_from_XL.xml' 
json_2013_target_by_country = '../output/2013/extra/goods_by_country_from_XL.json' 
json_2013_target_by_good = '../output/2013/extra/goods_by_good_from_XL.json'

csv_2014_target = '../output/2014/extra/goods_from_XL.csv' 
xml_2014_target_by_country = '../output/2014/extra/goods_by_country_from_XL.xml' 
xml_2014_target_by_good = '../output/2014/extra/goods_by_good_from_XL.xml' 
json_2014_target_by_country = '../output/2014/extra/goods_by_country_from_XL.json' 
json_2014_target_by_good = '../output/2014/extra/goods_by_good_from_XL.json'

present = "X"
sp_chars = special_chars.build()

mappings = ["Country_Name", 
            "Good_Name", 
            "Child_Labor", 
            "Forced_Labor", 
            "Forced_Child_Labor"]    

csl = ISO_countries.build()   
base_year = 2013
regs = regions.build(base_year)         
secs = sectors.build(base_year)

def get_base_year():
	return base_year

def set_base_year(yr):
	base_year = yr
	return

def  build(year):
	goods = utility.from_excelsheet(utility.get_source_filename(year), 2, 1, mappings)
	results = include_extra(goods, year)
	return results

def set_regions(year):
	regs = regions.build(year)
	return

def set_sectors(year):
	secs = sectors.build(year)
	return

def include_extra(goods_list, yer):
	result = []
	if yer != get_base_year():
		set_sectors(yer)
		set_regions(yer)
		set_base_year(yer)
	for good in goods_list:
		g = OrderedDict()
		g['Country_Name'] = good['Country_Name']
		g['Country_ISO2'] = ISO_countries.ISO2_from_name(g['Country_Name'], csl)
		g['Country_ISO3'] = ISO_countries.ISO3_from_name(g['Country_Name'], csl)		
		if (g['Country_ISO2'] == utility.get_default_error()):
			print " No ISO2 was found for ", g['Country_Name']
		if (g['Country_ISO3'] == utility.get_default_error()):
			print " No ISO3 was found for ", g['Country_Name']
		g['Country_Region'] = regions.find_region_from_ISO3(g['Country_ISO3'], regs)
		g['Good_Name'] = good['Good_Name']
		g['Good_Sector'] = sectors.find_sector_from_name(g['Good_Name'], secs)
		g['Child_Labor'] = ( "Yes" if (good['Child_Labor'] == present) else "No" )
		g['Forced_Labor'] = ( "Yes" if (good['Forced_Labor'] == present) else "No" )
		g['Forced_Child_Labor'] = ( "Yes" if (good['Forced_Child_Labor'] == present) else "No" )
		result.append(g)
	return result

def get_good_tuples_for_country(goods_list, cty):
	good_tuples = []
	country = cty.strip()
	for num in range(0, len(goods_list)):
		good_tuple = OrderedDict()
		c = goods_list[num]['Country_Name'].strip()
		if  (c == country):
			good_tuple['Good_Name'] = str(goods_list[num]['Good_Name']).strip()
			good_tuple['Good_Sector'] = str(goods_list[num]['Good_Sector']).strip()
			good_tuple['Child_Labor'] = str(goods_list[num]['Child_Labor']).strip()
			good_tuple['Forced_Labor'] = str(goods_list[num]['Forced_Labor']).strip()
			good_tuple['Forced_Child_Labor'] = str(goods_list[num]['Forced_Child_Labor']).strip()
			good_tuples.append(good_tuple)
	return good_tuples	

def get_country_tuples_for_good(goods_list, good):
	countries = []
	good = good.strip()
	for num in range(0, len(goods_list)):
		country_tuple = OrderedDict()
		r = goods_list[num]
		g = str(r['Good_Name']).strip()
		if ( good.upper() == g.upper() ):
			country_tuple['Country_Name'] = str(r['Country_Name']).strip()
			country_tuple['Country_ISO2'] = str(r['Country_ISO2']).strip()
			country_tuple['Country_ISO3'] = str(r['Country_ISO3']).strip()
			country_tuple['Country_Region'] = str(r['Country_Region']).strip()
			country_tuple['Child_Labor'] = str(r['Child_Labor']).strip()
			country_tuple['Forced_Labor'] = str(r['Forced_Labor']).strip()
			country_tuple['Forced_Child_Labor'] = str(r['Forced_Child_Labor']).strip()
			countries.append(country_tuple)
	return countries


def to_xml_by_country(filename, goods_list):
	
	target = open(filename, 'w+')

	target.write(utility.get_xml_header()+"\n")
	target.write("<Country_List>\n")

	countries = []

	# Group by Country
	for n in range(0, len(goods_list)):
		row = goods_list[n]
		country = special_chars.xml_safe(str(row['Country_Name']).strip(), sp_chars)
		iso2 = str(row['Country_ISO2'])
		iso3 = str(row['Country_ISO3'])
		region = special_chars.xml_safe(str(row['Country_Region']), sp_chars)
		good = str(row['Good_Name']).strip()
		if 	(country not in countries):
			target.write("\t<Country>\n"+"\t\t<Country_Name>"+country+"</Country_Name>"+"\n")
			target.write("\t\t<Country_ISO2>"+iso2+"</Country_ISO2>"+"\n")
			target.write("\t\t<Country_ISO3>"+iso3+"</Country_ISO3>"+"\n")
			target.write("\t\t<Country_Region>"+region+"</Country_Region>"+"\n")
			good_tuples = get_good_tuples_for_country(goods_list, country)
			target.write("\t\t<Goods>\n")
			for c in range(0, len(good_tuples)):
				target.write("\t\t\t<Good>\n")
				target.write("\t\t\t\t\t"+"<Good_Name>"+special_chars.xml_safe(str(good_tuples[c]['Good_Name']),sp_chars)+"</Good_Name>\n")
				target.write("\t\t\t\t\t"+"<Good_Sector>"+special_chars.xml_safe(str(good_tuples[c]['Good_Sector']),sp_chars)+"</Good_Sector>\n")				
				target.write("\t\t\t\t\t"+"<Child_Labor>"+str(good_tuples[c]['Child_Labor'])+"</Child_Labor>\n")
				target.write("\t\t\t\t\t"+"<Forced_Labor>"+str(good_tuples[c]['Forced_Labor'])+"</Forced_Labor>\n")
				target.write("\t\t\t\t\t"+"<Forced_Child_Labor>"+str(good_tuples[c]['Forced_Child_Labor'])+"</Forced_Child_Labor>\n")
				target.write("\t\t\t</Good>\n")
			target.write("\t\t</Goods>\n")
			target.write("\t</Country>\n")
			countries.append(country)
	target.write("</Country_List>\n")
	target.close()
	return

def to_xml_by_good(filename, goods_list):
	
	target = open(filename, 'w+')

	# Write XML Header
	target.write(utility.get_xml_header()+"\n")
	target.write("<Good_List>\n")

	# Sets of attributes
	products = []

	# Group by Good
	for n in range(0, len(goods_list)):
		row = goods_list[n]
		country = special_chars.xml_safe(str(row['Country_Name']).strip(),sp_chars)
		good = special_chars.xml_safe(str(row['Good_Name']).strip(),sp_chars)
		good_sector = special_chars.xml_safe(str(row['Good_Sector']).strip(),sp_chars)
		if 	(good not in products):
			target.write("\t<Good>\n"+"\t\t<Good_Name>"+good+"</Good_Name>"+"\n")
			target.write("\t\t<Good_Sector>"+good_sector+"</Good_Sector>"+"\n")			
			countryset = get_country_tuples_for_good(goods_list, good)
			target.write("\t\t<Countries>\n")
			for count in range(0, len(countryset)):
				target.write("\t\t\t<Country>\n")
				target.write("\t\t\t\t"+"<Country_Name>"+special_chars.xml_safe(str(countryset[count]['Country_Name']),sp_chars)+"</Country_Name>\n")
				target.write("\t\t\t\t"+"<Country_ISO2>"+str(countryset[count]['Country_ISO2'])+"</Country_ISO2>\n")
				target.write("\t\t\t\t"+"<Country_ISO3>"+str(countryset[count]['Country_ISO3'])+"</Country_ISO3>\n")
				target.write("\t\t\t\t"+"<Country_Region>"+special_chars.xml_safe(str(countryset[count]['Country_Region']),sp_chars)+"</Country_Region>\n")
				target.write("\t\t\t\t"+"<Child_Labor>"+str(countryset[count]['Child_Labor'])+"</Child_Labor>\n")
				target.write("\t\t\t\t"+"<Forced_Labor>"+str(countryset[count]['Forced_Labor'])+"</Forced_Labor>\n")
				target.write("\t\t\t\t"+"<Forced_Child_Labor>"+str(countryset[count]['Forced_Child_Labor'])+"</Forced_Child_Labor>\n")
				target.write("\t\t\t</Country>\n")
			target.write("\t\t</Countries>\n")
			target.write("\t</Good>\n")
			products.append(good)
	target.write("</Good_List>\n")
	target.close()
	return

def group_by_good(goods_list):
	products = []
	seen = []
	for n in range(0, len(goods_list)):
		product = OrderedDict()
		row = goods_list[n]
		cname = str(row['Country_Name']).strip()
		good = str(row['Good_Name']).strip()
		if good not in seen:
			product['Good_Name'] = good
			product['Good_Sector'] = row['Good_Sector']
			product['Countries'] = get_country_tuples_for_good(goods_list, good)
			products.append(product)
			seen.append(good)		
	return products

def group_by_country(goods_list):
	countries = []
	seen = []
	for n in range(0, len(goods_list)):
		country = OrderedDict()
		row = goods_list[n]
		cname = row['Country_Name']
		if cname not in seen:
			country['Country_Name'] = cname
			country['Country_ISO2'] = str(row['Country_ISO2'])
			country['Country_ISO3'] = str(row['Country_ISO3'])
			country['Country_Region'] = str(row['Country_Region'])
			country['Goods'] = get_good_tuples_for_country(goods_list, cname)
			countries.append(country)
			seen.append(cname)
	return countries

# Creates a JSON file for the data
def to_json(filename, data, groupby):
	# Correct this code
	if groupby == "C":
		jsondata = group_by_country(data)
	if groupby == "G":
		jsondata = group_by_good(data)
	utility.to_json(filename, jsondata)
	return

def to_xml(filename, data, groupby):
	success = False
	if groupby == "C":
		to_xml_by_country(filename, data)
	if groupby == "G":
		to_xml_by_good(filename, data)
	return

# Creates a CSV file for the data
def to_csv(filename, data):
	utility.to_csv_from_OD(filename, data)
	return


if __name__ == '__main__':
	
	goods_2013 = build(2013)
	goods_2014 = build(2014)

	to_csv(csv_2013_target, goods_2013)
	to_xml(xml_2013_target_by_good, goods_2013, "G")
	to_xml(xml_2013_target_by_country, goods_2013, "C")
	to_json(json_2013_target_by_country, goods_2013, "C")
	to_json(json_2013_target_by_good, goods_2013, "G")

	to_csv(csv_2014_target, goods_2014)
	to_xml(xml_2014_target_by_good, goods_2014, "G")
	to_xml(xml_2014_target_by_country, goods_2014, "C")
	to_json(json_2014_target_by_country, goods_2014, "C")
	to_json(json_2014_target_by_good, goods_2014, "G")



