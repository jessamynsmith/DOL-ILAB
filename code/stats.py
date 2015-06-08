

import utility
import ISO_countries 
import regions
from collections import OrderedDict

csv_target = '../output/country_stats_from_XL_2013.csv' 
xml_target = '../output/country_stats_from_XL_2013.xml' 
json_target = '../output/country_stats_from_XL_2013.json' 

CWS = "Children Work Statistics"
ESAS = "Education Statistics: Attendance Statistics"
CWAS = "Children Working and Studying (7-14 yrs old)"
UPCR = "UNESCO Primary Completion Rate"

regs = regions.build()
csl = ISO_countries.build()

mappings = [ 'Country_Name', 'Survey_Name', 
              CWS+' : Year', CWS+' : Survey Source', CWS+' : Age Range', 
              CWS+' : Total %', CWS+' : Total Working Population', 
              CWS+' : Agriculture', CWS+' : Service', CWS+' : Industry', 
              ESAS+' : Year', ESAS+' : Age Range', ESAS+' : %', 
              CWAS+' : Year', CWAS+' : Age Range', CWAS+' : Total', 
              UPCR+' : Year', UPCR+' : Rate' 
              ]


def build():
	master_data = utility.from_excelsheet(utility.get_source_filename(), 3, 3, mappings)
	results = include_extra(master_data)
	return results

def build_ordered():
	interim = build()
	result = order_by_country(interim)
	return result


def include_extra(masterdata):
	md_list = []
	for mdrec in masterdata:
	    md = OrderedDict()
	    md['Country_Name'] = mdrec['Country_Name']
	    md['Country_ISO2'] = ISO_countries.ISO2_from_name(md['Country_Name'], csl)
	    md['Country_ISO3'] = ISO_countries.ISO3_from_name(md['Country_Name'], csl)

	    if ( md['Country_ISO2'] == utility.get_default_error() ):
	    	print "There is no ISO2 for ", md['Country_Name']
	    if ( md['Country_ISO3'] == utility.get_default_error() ):
	    	print "There is no ISO3 for ", md['Country_Name']

	    md['Country_Region'] = regions.find_region_from_ISO3(md['Country_ISO3'], regs)
	    md['Survey_Name'] = mdrec['Survey_Name']
	    md[CWS+' : Year'] = mdrec[CWS+' : Year']
	    md[CWS+' : Survey Source'] = mdrec[CWS+' : Survey Source']
	    md[CWS+' : Age Range'] = mdrec[CWS+' : Age Range']
	    md[CWS+' : Total %'] = mdrec[CWS+' : Total %']
	    md[CWS+' : Total Working Population'] = mdrec[CWS+' : Total Working Population']
	    md[CWS+' : Agriculture'] = mdrec[CWS+' : Agriculture']
	    md[CWS+' : Service'] = mdrec[CWS+' : Service']
	    md[CWS+' : Industry'] = mdrec[CWS+' : Industry']
	    md[ESAS+' : Year'] = mdrec[ESAS+' : Year']
	    md[ESAS+' : Age Range'] = mdrec[ESAS+' : Age Range']
	    md[ESAS+' : %'] = mdrec[ESAS+' : %']
	    md[CWAS+' : Year'] = mdrec[CWAS+' : Year']
	    md[CWAS+' : Age Range'] = mdrec[CWAS+' : Age Range']
	    md[CWAS+' : Total'] = mdrec[CWAS+' : Total']
	    md[UPCR+' : Year'] = mdrec[UPCR+' : Year']
	    md[UPCR+' : Rate'] = mdrec[UPCR+' : Rate']
	    md_list.append(md)
	return md_list

def write_record(target, md):

	#print md, "\n"

	target.write("\t<Country>\n")

	target.write("\t\t<Country_Name>")
	target.write(md['Country_Name'])
	target.write("</Country_Name>\n")

	target.write("\t\t<Country_ISO2>")
	target.write(str(md['Country_ISO2']))
	target.write("</Country_ISO2>\n")

	target.write("\t\t<Country_ISO3>")
	target.write(str(md['Country_ISO3']))
	target.write("</Country_ISO3>\n")

	target.write("\t\t<Country_Region>")
	target.write(str(md['Country_Region']))
	target.write("</Country_Region>\n")


	target.write("\t\t<Survey_Name>")
	target.write(md['Survey_Name'])
	target.write("</Survey_Name>\n")

	target.write("\t\t<Childrens_Work_Statistics>\n")
	target.write("\t\t\t<Year>")
	target.write(md[CWS+' : Year'])
	target.write("</Year>\n")
	target.write("\t\t\t<Survey_Score>")
	target.write(md[CWS+' : Survey Source'])
	target.write("</Survey_Score>\n")
	target.write("\t\t\t<Age_Range>")
	target.write(md[CWS+' : Age Range'])
	target.write("</Age_Range>\n")
	target.write("\t\t\t<Total_Percentage_of_Working_Children>")
	target.write(str(md[CWS+' : Total %']))
	target.write("</Total_Percentage_of_Working_Children>\n")
	target.write("\t\t\t<Total_Working_Population>")
	target.write(str(md[CWS+' : Total Working Population']))
	target.write("</Total_Working_Population>\n")
	target.write("\t\t\t<Agriculture>")
	target.write(str(md[CWS+' : Agriculture']))
	target.write("</Agriculture>\n")
	target.write("\t\t\t<Service>")
	target.write(str(md[CWS+' : Service']))
	target.write("</Service>\n")
	target.write("\t\t\t<Industry>")
	target.write(str(md[CWS+' : Industry']))
	target.write("</Industry>\n")
	target.write("\t\t</Childrens_Work_Statistics>\n")
	
	target.write("\t\t<Education_Statistics_Attendance_Statistics>\n")
	target.write("\t\t\t<Year>")
	target.write(md[ESAS+' : Year'])
	target.write("</Year>\n")
	target.write("\t\t\t<Age_Range>")
	target.write(md[ESAS+' : Age Range'])
	target.write("</Age_Range>\n")
	target.write("\t\t\t<Percentage>")
	target.write(md[ESAS+' : %'])
	target.write("</Percentage>\n")
	target.write("\t\t</Education_Statistics_Attendance_Statistics>\n")

	target.write("\t\t<Children_Work_And_Studying>\n")
	target.write("\t\t\t<Year>")
	target.write(md[CWAS+' : Year'])
	target.write("</Year>\n")
	target.write("\t\t\t<Age_Range>")
	target.write(md[CWAS+' : Age Range'])
	target.write("</Age_Range>\n")
	target.write("\t\t\t<Total>")
	target.write(md[CWAS+' : Total'])
	target.write("</Total>\n")
	target.write("\t\t</Children_Work_And_Studying>\n")

	target.write("\t\t<Unesco_Primary_Completion_Rate>\n")
	target.write("\t\t\t<Year>")
	target.write(md[UPCR+' : Year'])
	target.write("</Year>\n")
	target.write("\t\t\t<Rate>")
	target.write(md[UPCR+' : Rate'])
	target.write("</Rate>\n")
	target.write("\t\t</Unesco_Primary_Completion_Rate>\n")

	target.write("\t</Country>\n")
	return

def to_xml(filename, mlist):
	target = open(filename, 'w+')
	target.write(utility.get_xml_header()+"\n")
	target.write("<Country_Statistics>\n")
	for country_record in mlist:
		write_record(target, country_record)
	target.write("</Country_Statistics>\n")
	target.close()
	return

def to_json(filename, data):
	jsondata = order_by_country(data)
	utility.to_json(filename, jsondata)
	return


def to_csv(filename, data):
	utility.to_csv_from_OD(filename, data)
	return


def order_by_country(mdlist):

	result = []

	for mdrec in mdlist:
		md = OrderedDict()
		md['Country_Name'] = mdrec['Country_Name']
		md['Country_ISO2'] = mdrec['Country_ISO2']
		md['Country_ISO3'] = mdrec['Country_ISO3']
		md['Country_Region'] = mdrec['Country_Region']
		md['Survey_Name'] = mdrec['Survey_Name']
		md[CWS] = []

		newcws = OrderedDict()
		newcws['Year'] = mdrec[CWS+' : Year']
		newcws['Survey Source'] = mdrec[CWS+' : Survey Source']
		newcws['Age Range'] = mdrec[CWS+' : Age Range']
		newcws['Total %'] = mdrec[CWS+' : Total %']
		newcws['Total Working Population'] = mdrec[CWS+' : Total Working Population']
		newcws['Agriculture'] = mdrec[CWS+' : Agriculture']
		newcws['Service'] = mdrec[CWS+' : Service']
		newcws['Industry'] = mdrec[CWS+' : Industry']
		md[CWS].append(newcws)

		md[ESAS] = []
		newesas = OrderedDict()
		newesas['Year'] = mdrec[ESAS+' : Year']
		newesas['Age Range'] = mdrec[ESAS+' : Age Range']
		newesas['%'] = mdrec[ESAS+' : %']
		md[ESAS].append(newesas)

		md[CWAS] = []
		newcwas = OrderedDict()
		newcwas['Year'] = mdrec[CWAS+' : Year']
		newcwas['Age Range'] = mdrec[CWAS+' : Age Range']
		newcwas['Total'] = mdrec[CWAS+' : Total']
		md[CWAS].append(newcwas)

		md[UPCR] = []
		newupcr = OrderedDict()
		newupcr['Year'] = mdrec[UPCR+' : Year']
		newupcr['Rate'] = mdrec[UPCR+' : Rate']
		md[UPCR].append(newupcr)
		result.append(md)

	return result

if __name__ == '__main__':
	
	mdlist = build()

	to_xml(xml_target, mdlist)
	to_json(json_target, mdlist)
	to_csv(csv_target, mdlist)
