

import utility
import ISO_countries 
import regions
import special_chars
from collections import OrderedDict

csv_target = '../output/extra/country_stats_from_XL_2013.csv' 
xml_target = '../output/extra/country_stats_from_XL_2013.xml' 
json_target = '../output/extra/country_stats_from_XL_2013.json' 

CWS = "Children_Work_Statistics"
ESAS = "Education_Statistics_Attendance_Statistics"
CWAS = "Children_Working_and_Studying_7-14_yrs_old"
UPCR = "UNESCO_Primary_Completion_Rate"

regs = regions.build()
csl = ISO_countries.build()
sp_chars = special_chars.build()

mappings = [ 'Country_Name', 'Survey_Name', 
              CWS+'_Year', CWS+'_Survey_Source', CWS+'_Age_Range', CWS +'_Total_Child_Population',
              CWS+'_Total_Percentage_of_Working_Children', CWS+'_Total_Working_Population', 
              CWS+'_Agriculture', CWS+'_Service', CWS+'_Industry', 
              ESAS+'_Year', ESAS+'_Age_Range', ESAS+'_Percentage', 
              CWAS+'_Year', CWAS+'_Age_Range', CWAS+'_Total', 
              UPCR+'_Year', UPCR+'_Rate' 
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
	    md[CWS+'_Year'] = mdrec[CWS+'_Year']
	    md[CWS+'_Survey_Source'] = mdrec[CWS+'_Survey_Source']
	    md[CWS+'_Age_Range'] = mdrec[CWS+'_Age_Range']
	    md[CWS +'_Total_Child_Population'] = mdrec[CWS +'_Total_Child_Population']
	    md[CWS+'_Total_Percentage_of_Working_Children'] = mdrec[CWS+'_Total_Percentage_of_Working_Children']
	    md[CWS+'_Total_Working_Population'] = mdrec[CWS+'_Total_Working_Population']
	    md[CWS+'_Agriculture'] = mdrec[CWS+'_Agriculture']
	    md[CWS+'_Service'] = mdrec[CWS+'_Service']
	    md[CWS+'_Industry'] = mdrec[CWS+'_Industry']
	    md[ESAS+'_Year'] = mdrec[ESAS+'_Year']
	    md[ESAS+'_Age_Range'] = mdrec[ESAS+'_Age_Range']
	    md[ESAS+'_Percentage'] = mdrec[ESAS+'_Percentage']
	    md[CWAS+'_Year'] = mdrec[CWAS+'_Year']
	    md[CWAS+'_Age_Range'] = mdrec[CWAS+'_Age_Range']
	    md[CWAS+'_Total'] = mdrec[CWAS+'_Total']
	    md[UPCR+'_Year'] = mdrec[UPCR+'_Year']
	    md[UPCR+'_Rate'] = mdrec[UPCR+'_Rate']
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
	target.write(special_chars.xml_safe(str(md['Country_Region']),sp_chars))
	target.write("</Country_Region>\n")


	target.write("\t\t<Survey_Name>")
	target.write(md['Survey_Name'])
	target.write("</Survey_Name>\n")

	target.write("\t\t<Childrens_Work_Statistics>\n")
	target.write("\t\t\t<Year>")
	target.write(md[CWS+'_Year'])
	target.write("</Year>\n")
	target.write("\t\t\t<Survey_Score>")
	target.write(md[CWS+'_Survey_Source'])
	target.write("</Survey_Score>\n")
	target.write("\t\t\t<Age_Range>")
	target.write(md[CWS+'_Age_Range'])
	target.write("</Age_Range>\n")
	target.write("\t\t\t<Total_Child_Population>")
	target.write(md[CWS +'_Total_Child_Population'])
	target.write("\t\t\t</Total_Child_Population>\n")
	target.write("\t\t\t<Total_Percentage_of_Working_Children>")
	target.write(str(md[CWS+'_Total_Percentage_of_Working_Children']))
	target.write("</Total_Percentage_of_Working_Children>\n")
	target.write("\t\t\t<Total_Working_Population>")
	target.write(str(md[CWS+'_Total_Working_Population']))
	target.write("</Total_Working_Population>\n")
	target.write("\t\t\t<Agriculture>")
	target.write(str(md[CWS+'_Agriculture']))
	target.write("</Agriculture>\n")
	target.write("\t\t\t<Service>")
	target.write(str(md[CWS+'_Service']))
	target.write("</Service>\n")
	target.write("\t\t\t<Industry>")
	target.write(str(md[CWS+'_Industry']))
	target.write("</Industry>\n")
	target.write("\t\t</Childrens_Work_Statistics>\n")
	
	target.write("\t\t<Education_Statistics_Attendance_Statistics>\n")
	target.write("\t\t\t<Year>")
	target.write(md[ESAS+'_Year'])
	target.write("</Year>\n")
	target.write("\t\t\t<Age_Range>")
	target.write(md[ESAS+'_Age_Range'])
	target.write("</Age_Range>\n")
	target.write("\t\t\t<Percentage>")
	target.write(md[ESAS+'_Percentage'])
	target.write("</Percentage>\n")
	target.write("\t\t</Education_Statistics_Attendance_Statistics>\n")

	target.write("\t\t<Children_Work_And_Studying>\n")
	target.write("\t\t\t<Year>")
	target.write(md[CWAS+'_Year'])
	target.write("</Year>\n")
	target.write("\t\t\t<Age_Range>")
	target.write(md[CWAS+'_Age_Range'])
	target.write("</Age_Range>\n")
	target.write("\t\t\t<Total>")
	target.write(md[CWAS+'_Total'])
	target.write("</Total>\n")
	target.write("\t\t</Children_Work_And_Studying>\n")

	target.write("\t\t<Unesco_Primary_Completion_Rate>\n")
	target.write("\t\t\t<Year>")
	target.write(md[UPCR+'_Year'])
	target.write("</Year>\n")
	target.write("\t\t\t<Rate>")
	target.write(md[UPCR+'_Rate'])
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
		newcws['Year'] = mdrec[CWS+'_Year']
		newcws['Survey_Source'] = mdrec[CWS+'_Survey_Source']
		newcws['Age_Range'] = mdrec[CWS+'_Age_Range']
		newcws['Total_Child_Population'] = mdrec[CWS +'_Total_Child_Population']
		newcws['Total_Percentage_of_Working_Children'] = mdrec[CWS+'_Total_Percentage_of_Working_Children']
		newcws['Total_Working_Population'] = mdrec[CWS+'_Total_Working_Population']
		newcws['Agriculture'] = mdrec[CWS+'_Agriculture']
		newcws['Service'] = mdrec[CWS+'_Service']
		newcws['Industry'] = mdrec[CWS+'_Industry']
		md[CWS].append(newcws)

		md[ESAS] = []
		newesas = OrderedDict()
		newesas['Year'] = mdrec[ESAS+'_Year']
		newesas['Age Range'] = mdrec[ESAS+'_Age_Range']
		newesas['Percentage'] = mdrec[ESAS+'_Percentage']
		md[ESAS].append(newesas)

		md[CWAS] = []
		newcwas = OrderedDict()
		newcwas['Year'] = mdrec[CWAS+'_Year']
		newcwas['Age Range'] = mdrec[CWAS+'_Age_Range']
		newcwas['Total'] = mdrec[CWAS+'_Total']
		md[CWAS].append(newcwas)

		md[UPCR] = []
		newupcr = OrderedDict()
		newupcr['Year'] = mdrec[UPCR+'_Year']
		newupcr['Rate'] = mdrec[UPCR+'_Rate']
		md[UPCR].append(newupcr)
		result.append(md)

	return result

if __name__ == '__main__':
	
	mdlist = build()

	to_xml(xml_target, mdlist)
	to_json(json_target, mdlist)
	to_csv(csv_target, mdlist)

	