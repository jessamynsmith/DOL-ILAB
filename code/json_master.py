
import json
import csv
from collections import OrderedDict
import add_iso2_to_goods_and_products
import merge_country_master_with_goods
import get_region

c_json_file = "../output/extra/countries_profile.json"

CWS = '''Children's Work Statistics'''
ESAS = "Education Statistics: Attendance Statistics"
CWAS = "Children Working and Studying (7-14 yrs old)"
UPCR = "UNESCO Primary Completion Rate"
year_last_report = 2013


def get_json_data():
	country_data = []
	with open(c_json_file) as json_file:
		country_data = json.load(json_file)
	return country_data

def get_master_data(mdlist, iso2, yr):
	result = []
	for n in range(0,len(mdlist)):
		if (mdlist[n]['ISO2'].strip() == iso2.strip()) and (yr == mdlist[n]['Year']):
			result = mdlist[n]
			break
	return result

def merge_data(cps, master):
	result = []

	regions = get_region.build()

	for cp in cps:
		nr = OrderedDict()
		nr['Country'] = cp['country'].encode('utf8')
		iso2 = add_iso2_to_goods_and_products.get_ISO2(nr['Country'])
		nr['Region'] = get_region.find_by_ISO2(iso2, regions)
		if nr['Region'] == -1:
			print "No region found for ", nr['Country']
		nr['ISO2'] = iso2
		nr['Advancement_Level'] = cp['advancement_level']
		nr['Description'] = cp['description']
		m = get_master_data(master, nr['ISO2'], year_last_report)
		#print "Master Data Entry for: ", nr['ISO2'], ", year ", year_last_report, " is ", m, "\n\n"
		if (m != []):
			nr['Year'] = m['Year']

			goodset = []
			for good in m['Goods']:
				ng = OrderedDict()
				ng['Good_Name'] = good[0]
				ng['Child_Labor'] = good[1]
				ng['Forced_Labor'] = good[2]
				ng['Forced_Child_Labor'] = good[3]
				goodset.append(ng)
			nr['Goods'] = goodset

			nr['Survey Name'] = m['Survey Name']

			cwsset = []
			nws = OrderedDict()
			nws['Year'] = m[CWS+' : Year']
			nws['Survey_Source'] = m[CWS+' : Survey Source']
			nws['Age_Range'] = m[CWS+' : Age Range']
			nws['Total_Child_Population'] = m[CWS+' : Total Child Population']
			nws['Total_Percentage_of_Working_Children'] = m[CWS+' : Total % of Working Children']
			nws['Total_Working_Population'] = m[CWS+' : Total Working Population']
			nws['Agriculture'] = m[CWS+' : Agriculture']
			nws['Service'] = m[CWS+' : Service']
			nws['Industry'] = m[CWS+' : Industry']
			cwsset.append(nws)
			nr[CWS] = cwsset

			eslist = []
			esl = OrderedDict()
			esl['Year'] = m[ESAS+' : Year']
			esl['Age_Range'] = m[ESAS+' : Age Range']
			esl['Percentage'] = m[ESAS+' : %']
			eslist.append(esl)
			nr[ESAS] = eslist


			cwaslist = []
			nc = OrderedDict()
			nc['Year'] = m[CWAS+' : Year']
			nc['Age_Range'] = m[CWAS+' : Age Range']
			nc['Age_Range'] = m[CWAS+' : Total']
			cwaslist.append(nc)
			nr[CWAS] = cwaslist

			upcrlist = []
			nu = OrderedDict()
			nu['Year'] = m[UPCR+' : Year']
			nu['Rate'] = m[UPCR+' : Rate']
			upcrlist.append(nu)
			nr[UPCR] = upcrlist

			nr['Sources'] = cp['sources']
			nr['Tables'] = cp['tables']
		result.append(nr)
		#print "Country Profile for: ", nr['ISO2'], ", year ", year_last_report, " is ", nr, "\n\n"

	return result

def to_json(clist, fname):
	j = json.dumps(clist) 	
	with open(fname, 'w+') as f:
	    f.write(j)
	return


if __name__ == '__main__':

	country_profiles = get_json_data()
	master_data = merge_country_master_with_goods.build()

	profiles = merge_data(country_profiles, master_data)

	to_json(profiles, "../output/countries.json")


