import utility 
import ISO_countries
import special_chars
from collections import OrderedDict

json_2013_target = '../output/2013/extra/country_region_mappings.json' 
csv_2013_target = '../output/2013/extra/country_region_mappings.csv' 
xml_2013_target = '../output/2013/extra/country_region_mappings.xml' 

json_2014_target = '../output/2014/extra/country_region_mappings.json' 
csv_2014_target = '../output/2014/extra/country_region_mappings.csv' 
xml_2014_target = '../output/2014/extra/country_region_mappings.xml' 

mappings = ["Country_Name", "Country_Region"]    # Info to be extracted from spreadsheet

isocountries = ISO_countries.build()
sp_chars = special_chars.build()

def include_ISO(rlist):
	result = []
	for r in rlist:
		row = OrderedDict()
		cn = r['Country_Name']
		row['Country_Name'] = cn
		row['Country_ISO2'] = ISO_countries.ISO2_from_name(cn, isocountries)
		row['Country_ISO3'] = ISO_countries.ISO3_from_name(cn, isocountries)	
		row['Country_Region'] = r['Country_Region']
		result.append(row)
	return result

def build(year):
	regs = utility.from_excelsheet(utility.get_source_filename(year), 0, 1, mappings)
	results = include_ISO(regs)
	return results

def find_region_from_name(name, reglist):
	result = find_X_from_name(name, reglist, "Country_Region")
	return result

def find_ISO2_from_name(name, reglist):
	result = find_X_from_name(name, reglist, "Country_ISO2")
	return result

def find_ISO3_from_name(name, reglist):
	result = find_X_from_name(name, reglist, "Country_ISO3")
	return result

def find_X_from_name(name, reglist, tag):
	result = utility.get_default_error()
	cname = name.upper().strip()
	for reg in reglist:
		try:
			pname = reg['Country_Name'].encode('utf-8').upper().strip()
		except UnicodeDecodeError:
			pname = reg['Country_Name'].upper().strip()
		if (pname == cname):
			result = reg[tag]
			break
	return result

def find_X_from_Y(tag1, tag2, reglist, request):  
	result = utility.get_default_error()
	req = request.upper().strip()
	for reg in reglist:
		try:
			pvar = reg[tag2].encode('utf-8').upper().strip()
		except UnicodeDecodeError:
			pvar = reg[tag2].upper().strip()
		if (pvar == req):
			result = reg[tag1]
			break	
	return result

def find_region_from_ISO2(i2, reglist):
	result = utility.get_default_error()
	for reg in reglist:
		if (reg['Country_ISO2'] != utility.get_default_error()) and (reg['Country_ISO2'].upper().strip() == i2.upper().strip()):
			result = reg['Country_Region']
			break
	return result

def find_region_from_ISO3(i3, reglist):
	result = utility.get_default_error()
	for reg in reglist:
		if (reg['Country_ISO3'] != utility.get_default_error()) and (reg['Country_ISO3'].upper().strip() == i3.upper().strip()):
			result = reg['Country_Region']
			break
	return result

# Creates a JSON file for the data
def to_json(filename, data):
	utility.to_json(filename, data)
	return

# Creates a CSV file for the data
def to_csv(filename, data):
	utility.to_csv_from_OD(filename, data)
	return

def to_xml(filename, data):	
	target = open(filename, 'w+')
	target.write(utility.get_xml_header()+"\n")
	target.write("<Countries>\n")
	for country in data:
		target.write("\t<Country>\n")
		target.write("\t\t<Country_Name>"+special_chars.xml_safe(country['Country_Name'],sp_chars)+"</Country_Name>\n")
		target.write("\t\t<Country_ISO2>"+str(country['Country_ISO2'])+"</Country_ISO2>\n")
		target.write("\t\t<Country_ISO3>"+str(country['Country_ISO3'])+"</Country_ISO3>\n")
		target.write("\t\t<Country_Region>"+special_chars.xml_safe(country['Country_Region'],sp_chars)+"</Country_Region>\n")						
		target.write("\t</Country>\n")
	target.write("</Countries>\n")
	target.close()
	return

if __name__ == '__main__':
	regions_2013 = build(2013)
	regions_2014 = build(2014)

	to_json(json_2013_target, regions_2013)
	to_csv(csv_2013_target, regions_2013)
	to_xml(xml_2013_target, regions_2013)

	to_json(json_2014_target, regions_2014)
	to_csv(csv_2014_target, regions_2014)
	to_xml(xml_2014_target, regions_2014)





