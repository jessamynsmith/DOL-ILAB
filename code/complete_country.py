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
xml_target = "../output/countries_2013.xml"
json_for_app_target = "../output/countries_for_app_2013.json"
xml_for_app_target = "../output/countries_for_app_2013.xml"

suggested_actions_text = "Suggested Government Actions"


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
			if (ckeys[n] != "Goods") and (ckeys[n] != "Suggested_Actions"):
				for l in kv:
					write_record(target, l, count+1)
			if (ckeys[n] == "Goods"):
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
			if (ckeys[n] == "Suggested_Actions"):
				sga = cr[ckeys[n]]
				for action in sga:
					stripped = unicode(utility.unicode_to_str(action['Area']), 'ascii', 'ignore')
					xmltag = sanitize(utility.unicode_to_str(stripped))
					target.write( utility.tabs(count+1) + utility.create_starting_xml_tag(xmltag) + utility.get_newline() )
					for act in action['Actions']:
						target.write(utility.tabs(count+2) + utility.create_starting_xml_tag("Action") + utility.get_newline() )
						aname = special_chars.xml_safe(utility.unicode_to_str(act['Name']), sp_chars)
						ayears = special_chars.xml_safe(utility.unicode_to_str(act['Years']), sp_chars)
						target.write(utility.tabs(count+3) + utility.create_starting_xml_tag("Name")  
						             + aname + utility.create_closing_xml_tag("Name")
						             + utility.get_newline() )
						target.write(utility.tabs(count+3) + utility.create_starting_xml_tag("Years")  
						             + ayears + utility.create_closing_xml_tag("Years")
						             + utility.get_newline() )
						target.write(utility.tabs(count+2) + utility.create_closing_xml_tag("Action") + utility.get_newline() )
					target.write( utility.tabs(count+1) + utility.create_closing_xml_tag(xmltag) + utility.get_newline() )
			target.write( utility.tabs(count) + utility.create_closing_xml_tag(ckeys[n]) + utility.get_newline() )
		else:
			keyname = utility.to_str(ckeys[n])
			start = utility.create_starting_xml_tag(keyname)
			val = special_chars.xml_safe(utility.to_str(cr[keyname]), sp_chars)
			end = utility.create_closing_xml_tag(keyname)
			target.write( utility.tabs(count) + start + val + end + utility.get_newline() )
	return

def sanitize(stri):
	res = stri.strip().replace(".", "")
	res = res.replace(",", "")
	res = res.replace(" ","_")
	res = res.replace("-", "_")
	res = res.replace("(", "")
	res = res.replace(")", "")
	res = res.replace("_&_", "_and_")
	return res

def compact_data_for_app(data):
	results = []
	for record in data: 
		newrec = OrderedDict()
		newrec['Name'] = record['Name']
		newrec['Region'] = record['Region']
		newrec['ISO2'] = record['ISO2']
		newrec['ISO3'] = record['ISO3']
		newrec['Advancement_Level'] = record['Advancement_Level']
		newrec['Description'] = record['Description']
		newrec['Goods'] = record['Goods']
		newrec['Country_Statistics'] = record['Country_Statistics']
		newrec['Master_Data'] = record['Master_Data']
		newrec['Suggested_Actions'] = get_suggested_actions(record)	
		results.append(newrec)
	return results


def find_suggested_actions_section(country_record):
    count = -1
    sa_array = country_record['Sections']
    for section in sa_array:
    	count += 1
    	ctitle = utility.unicode_to_str(section['title'])
    	if (suggested_actions_text in ctitle ):
    		break
    	if (count == (len(sa_array) - 1)):
    		count = -1

    return count

def get_suggested_actions(country_record):
	actions = []
	index = find_suggested_actions_section(country_record)
	if (index != -1 ):
		areas = country_record['Sections'][index]['tables'][0]['areas']
		for cur_area in areas:
			newarea = OrderedDict()
			newarea['Area'] = cur_area['area']
			newarea['Actions'] = []
			cur_actions = cur_area['actions']
			agglist = []
			for cur_action in cur_actions:
				newaction = OrderedDict()
				newaction['Name'] = cur_action['action']
				newaction['Years'] = cur_action['years']
				agglist.append(newaction)
			if len(agglist) != 0:
				newarea['Actions'] = agglist
			actions.append(newarea)
	return actions

if __name__ == '__main__':

	cost = build()
	app_cost = compact_data_for_app(cost)

	to_json(json_target, cost)
	to_xml(xml_target, cost)
	to_json(json_for_app_target, app_cost)
	to_xml(xml_for_app_target, app_cost)



