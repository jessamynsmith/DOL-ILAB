import goods
import stats
import master_data
import utility
import ISO_countries
import regions
from collections import OrderedDict

source_json_file = "../source_data/country_profile.json"

json_target = "../output/countries_2013.json"
csv_target = "../output/countries_2013.csv"
xml_target = "../output/countries_2013.xml"


mds = master_data.build()
sts = stats.build_ordered()
gds = goods.build()
csl = ISO_countries.build()
regs = regions.build()
cps = utility.get_json_data(source_json_file)

def build():
	countries = merge(cps, gds, sts, mds)
	return countries

def add_to_country_profiles(profiles):
	results = []
	cpkeys = profiles[0].keys()
	for profile in profiles:
		newrec = OrderedDict()
		cn = profile['country'].encode('utf8')
		newrec['Country_ISO3'] = ISO_countries.ISO3_from_name(cn, csl)
		if ( newrec['Country_ISO3'] == utility.get_default_error() ):
			print "Could not find ISO3 for ", cn
		for n in range(0, len(cpkeys)):
			cur = cpkeys[n]
			newrec[cur] = profile[cur]
		results.append(newrec)
	return results


def merge(cps, gds, statistics, master_data):
	results = []
	country_profiles = add_to_country_profiles(cps)
	stats_attribs = statistics[0].keys()
	md_attribs = master_data[0].keys()
	for c in regs:
		nr = combine(c, gds, country_profiles, mds, sts, stats_attribs, md_attribs)
		results.append(nr)
	return results

def combine(c, gds, country_profiles, mds, sts, stats_attribs, md_attribs):
	newrow = OrderedDict()
	country_name = c['Country_Name']
	iso2 = c['Country_ISO2']
	iso3 = c['Country_ISO3']
	region = c['Country_Region']
	this_cp = utility.get_tuple_by_X(iso3, "Country_ISO3", country_profiles)
	this_md = utility.get_tuple_by_X(iso3, "Country_ISO3", mds)
	this_sts = utility.get_tuple_by_X(iso3, "Country_ISO3", sts)
	this_goods = goods.get_good_tuples_for_country(gds, country_name)
	cpkeys = this_cp.keys()
	skeys = this_sts.keys()
	mkeys = this_md.keys()	
	advancement =  ( this_cp['advancement_level'] if (len(cpkeys) != 0) else "" )
	#print "GOT HERE ", country_name
	description = ( this_cp['description'] if (len(cpkeys) != 0) else "" )
	tables = (this_cp['tables'] if (len(cpkeys) != 0) else [])
	sources = ( this_cp['sources'] if (len(cpkeys) != 0) else [])
	newrow['Name'] = country_name
	newrow['Region'] = region
	newrow['ISO2'] = iso2
	newrow['ISO3'] = iso3
	newrow['Advancement_Level'] = advancement
	newrow['Description'] = description
	newrow['Goods'] = this_goods
	#print "GOT HERE ", country_name	
	#print " Current Keys for Stats is ", skeys
	if (skeys != 0):
		for count in range(4,len(stats_attribs)):
			curkey = stats_attribs[count]
			try:
				newrow[curkey] = this_sts[curkey]
			except KeyError:
				newrow[curkey] = ""
	if (mkeys != 0):
		for newcount in range(5,len(md_attribs)):
			curkey = md_attribs[newcount]
			try:
				newrow[curkey] = this_md[curkey]
			except KeyError:
				newrow[curkey] = ""
	newrow['Tables'] = tables
	newrow['Sources'] = sources
	return newrow

def to_json(filename, data):
	utility.to_json(filename, data)
	return


def to_csv(filename, data):
	utility.to_csv_from_OD(filename, data)
	return

def to_xml(filename, data):
	target = open(filename, 'w+')
	target.write(utility.get_xml_header() + utility.get_newline())
	target.write("<Countries>" + utility.get_newline())
	for country_record in data:
		target.write( utility.tabs(1) + utility.create_starting_xml_tag("Country") + utility.get_newline())
		utility.write_record(target, country_record, 2)
		target.write( utility.tabs(1) + utility.create_closing_xml_tag("Country") + utility.get_newline() )
	target.write("</Countries>" + utility.get_newline())
	target.close()
	return



if __name__ == '__main__':

	cost = build()

	#print cost

	to_json(json_target, cost)
	to_xml(xml_target, cost)


	#to_csv(csv_target, cost)


