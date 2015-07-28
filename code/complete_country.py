import goods
import stats
import master_data
import utility
import ISO_countries
import regions
import special_chars
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
sp_chars = special_chars.build()

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
	description = ( this_cp['description'] if (len(cpkeys) != 0) else "" )
	sections = (this_cp['sections'] if (len(cpkeys) != 0) else [])
	sources = ( this_cp['sources'] if (len(cpkeys) != 0) else [])
	newrow['Name'] = country_name
	newrow['Region'] = region
	newrow['ISO2'] = iso2
	newrow['ISO3'] = iso3
	newrow['Advancement_Level'] = advancement
	newrow['Description'] = description
	newrow['Goods'] = this_goods 

	newrow['Country_Statistics'] = []
	sfound = False if ( stats.found_stats_from(iso3, "Country_ISO3", sts) == utility.get_default_error()) else True
	if not sfound:
		print " No Country Statistics for ", country_name 
	if (skeys != 0) and (sfound) :
		nray = []
		for count in range(4,len(stats_attribs)):
			nr = OrderedDict()
			curkey = stats_attribs[count]
			try:
				nr[curkey] = this_sts[curkey]
			except KeyError:
				nr[curkey] = ""
			nray.append(nr)
		newrow['Country_Statistics'] = nray
	newrow['Master_Data'] = []
	mfound = False if (master_data.found_master_data_from(iso3, "Country_ISO3", mds) == utility.get_default_error()) else True
	if not mfound:
		print " No Master Data for ", country_name 
	if (mkeys != 0) and (mfound):
		mray = []
		for newcount in range(5,len(md_attribs)):
			nr = OrderedDict()
			curkey = md_attribs[newcount]
			try:
				nr[curkey] = this_md[curkey]
			except KeyError:
				nr[curkey] = ""
			mray.append(nr)
		newrow['Master_Data'] = mray
	newrow['Sections'] = sections
	newrow['Sources'] = sources
	return newrow

def to_json(filename, data):
	utility.to_json(filename, data)
	return


def to_xml(filename, data):
	target = open(filename, 'w+')
	target.write(utility.get_xml_header() + utility.get_newline())
	target.write("<Countries>" + utility.get_newline())
	for country_record in data:
		target.write( utility.tabs(1) + utility.create_starting_xml_tag("Country") + utility.get_newline())
		write_record(target, country_record, 2)
		target.write( utility.tabs(1) + utility.create_closing_xml_tag("Country") + utility.get_newline() )
	target.write("</Countries>" + utility.get_newline())
	target.close()
	return

def write_record(target, cr, count): 
	ckeys = cr.keys()
	for n in range(0, len(cr)): 
		kv = cr[ckeys[n]]
		if (type(kv) == list):
			target.write( utility.tabs(count) + utility.create_starting_xml_tag(ckeys[n]) + utility.get_newline() )
			#count += 1
			if ckeys[n] != "Goods":
				for l in kv:
					write_record(target, l, count+1)
				#count -= 1
			else:
				for good in cr[ckeys[n]]:
					target.write( utility.tabs(count+1) + "<Good>" + utility.get_newline() )
					target.write( utility.tabs(count+2) + utility.create_starting_xml_tag("Good_Name"))
					target.write( good["Good_Name"])
					target.write( utility.create_closing_xml_tag("Good_Name") + utility.get_newline() )
					target.write( utility.tabs(count+2) + utility.create_starting_xml_tag("Child_Labor") )
					target.write( good["Child_Labor"] )
					target.write( utility.create_closing_xml_tag("Child_Labor") + utility.get_newline() )
					target.write( utility.tabs(count+2) + utility.create_starting_xml_tag("Forced_Labor") )
					target.write( good["Forced_Labor"]  )
					target.write( utility.create_closing_xml_tag("Forced_Labor") + utility.get_newline() )
					target.write( utility.tabs(count+2) + utility.create_starting_xml_tag("Forced_Child_Labor")  )
					target.write( good["Forced_Child_Labor"]  )
					target.write( utility.create_closing_xml_tag("Forced_Child_Labor") + utility.get_newline() )
					target.write( utility.tabs(count+1) + "</Good>" + utility.get_newline() )
				#count -= 1
			target.write( utility.tabs(count) + utility.create_closing_xml_tag(ckeys[n]) + utility.get_newline() )
		else:
			keyname = utility.to_str(ckeys[n])
			start = utility.create_starting_xml_tag(keyname)
			val = special_chars.xml_safe(utility.to_str(cr[keyname]), sp_chars)
			end = utility.create_closing_xml_tag(keyname)
			target.write( utility.tabs(count) + start + val + end + utility.get_newline() )
	return



if __name__ == '__main__':

	cost = build()

	to_json(json_target, cost)
	to_xml(xml_target, cost)


