import utility
import goods
import sectors
import special_chars
from collections import OrderedDict

csv_target = '../output/goods.csv' 
xml_target = '../output/goods_by_good_2013.xml' 
json_target = '../output/goods_by_good_2013.json'

secs = sectors.build()
gds = goods.build()
sp_chars = special_chars.build()

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
		write_record(target, good_record, 2)
		target.write( utility.tabs(1) + utility.create_closing_xml_tag("Good")  + utility.get_newline() )
	target.write("</Goods>" + utility.get_newline())
	target.close()
	return


def write_record(target, cr, count): 
	ckeys = cr.keys()
	for n in range(0, len(cr)): 
		kv = cr[ckeys[n]]
		if (type(kv) == list):
			target.write( utility.tabs(count) + utility.create_starting_xml_tag(ckeys[n]) + utility.get_newline() )
			count += 1
			for l in kv:
				this_key_group = (ckeys[n])[:(len(ckeys[n])-1)]
				if len(kv) > 0:
					this_key_group = this_key_group.replace("ie", "y")
					#print this_key_group
					target.write( utility.tabs(count) + utility.create_starting_xml_tag(this_key_group) + utility.get_newline())
				write_record(target, l, count+1)
				if len(kv) > 0:
					target.write( utility.tabs(count) + utility.create_closing_xml_tag(this_key_group) + utility.get_newline())
			target.write( utility.tabs(count) + utility.create_closing_xml_tag(ckeys[n]) + utility.get_newline() )
		else:
			keyname = utility.to_str(ckeys[n])
			start = utility.create_starting_xml_tag(keyname)
			val = special_chars.xml_safe(utility.to_str(cr[keyname]), sp_chars)
			end = utility.create_closing_xml_tag(keyname)
			target.write( utility.tabs(count) + start + val + end + utility.get_newline() )
	return

if __name__ == '__main__':
	cgoods = build()

	#print cgoods

	to_json(json_target, cgoods)
	to_xml(xml_target, cgoods)



