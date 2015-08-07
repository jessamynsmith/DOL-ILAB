
import utility
import special_chars

json_2013_target = '../output/2013/extra/good_sector_mappings.json' 
csv_2013_target = '../output/2013/extra/good_sector_mappings.csv' 
xml_2013_target = '../output/2013/extra/good_sector_mappings.xml' 

json_2014_target = '../output/2014/extra/good_sector_mappings.json' 
csv_2014_target = '../output/2014/extra/good_sector_mappings.csv' 
xml_2014_target = '../output/2014/extra/good_sector_mappings.xml' 

mappings = ["Good_Sector", "Good_Name"]   #The attributes to be extracted from the spreadsheet

sp_chars = special_chars.build()

# Function that returns the sector associated with a good name (otherwise it returns -1)
def find_sector_from_name(goodname, slist):
	result = utility.get_default_error()
	ig = utility.canonical_good(goodname).upper().strip()
	for s in slist:
		cg = utility.canonical_good(s['Good_Name']).upper().strip()
		if (utility.goods_equal(ig, cg)):
			result = s['Good_Sector']
			break
	return result

# Function that returns a sorted list of the goods in a particular sector
def find_goods_in_sector(sector, slist):
	result = utility.get_default_error()
	searchstring = sector.upper().strip()
	runner = []
	for sec in slist:
		if (searchstring == (sec['Good_Sector'].upper().strip())):
			cg = utility.canonical_good(sec['Good_Name']).strip()
			if (cg not in runner):
				runner.append(sec['Good_Name'].strip())
	if (len(runner) > 0):
		result = sorted(runner)
	return result

# Creates an Ordered Dictionary of Goods and their Associated Sectors
def build(year):
	result = utility.from_excelsheet(utility.get_source_filename(year), 1, 1, mappings)
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
	target.write("<Goods>\n")
	for good in data:
		target.write("\t<Good>\n")
		target.write("\t\t<Good_Name>"+special_chars.xml_safe(good['Good_Name'],sp_chars)+"</Good_Name>\n")
		target.write("\t\t<Good_Sector>"+special_chars.xml_safe(good['Good_Sector'],sp_chars)+"</Good_Sector>\n")
		target.write("\t</Good>\n")
	target.write("</Goods>\n")
	target.close()
	return


if __name__ == '__main__':
	sectors_2013 = build(2013)
	sectors_2014 = build(2014)

	to_json(json_2013_target, sectors_2013)
	to_csv(csv_2013_target, sectors_2013)
	to_xml(xml_2013_target, sectors_2013)

	to_json(json_2014_target, sectors_2014)
	to_csv(csv_2014_target, sectors_2014)
	to_xml(xml_2014_target, sectors_2014)







