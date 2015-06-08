import utility
import goods
import sectors
from collections import OrderedDict

csv_target = '../output/goods.csv' 
xml_target = '../output/goods_by_good_2013.xml' 
json_target = '../output/goods_by_good_2013.json'

secs = sectors.build()
gds = goods.build()

newline = "\n"


def build():
	results = []
	for sector in secs:
		newr = OrderedDict()
		newr['Good_Name'] = sector['Good_Name']
		newr['Good_Sector'] = sector['Good_Sector']
		newr['Countries'] = goods.get_country_tuples_for_good(gds,newr['Good_Name'])
		results.append(newr)
	return results
def to_json(filename, data):
	utility.to_json(filename, data)
	return


def to_xml(filename, data):
	target = open(filename, 'w+')
	target.write(utility.get_xml_header() + utility.get_newline())
	target.write("<Goods>" + utility.get_newline())
	for good_record in data:
		target.write( utility.tabs(1) + utility.create_starting_xml_tag("Good")  + utility.get_newline() )
		utility.write_record(target, good_record, 2)
		target.write( utility.tabs(1) + utility.create_closing_xml_tag("Good")  + utility.get_newline() )
	target.write("</Goods>" + utility.get_newline())
	target.close()
	return



if __name__ == '__main__':
	cgoods = build()

	print cgoods

	to_json(json_target, cgoods)
	to_xml(xml_target, cgoods)



