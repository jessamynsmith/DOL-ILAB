

import utility
import ISO_countries 
import regions
import special_chars
from collections import OrderedDict

csv_target = '../output/extra/country_stats_from_XL_2013.csv' 
xml_target = '../output/extra/country_stats_from_XL_2013.xml' 
json_target = '../output/extra/country_stats_from_XL_2013.json' 

CWS = "Children_Work_Statistics"
ESAS = "Education_Statistics:_Attendance_Statistics"
CWAS = "Children_Working_and_Studying_7-14_yrs_old"
UPCR = "UNESCO_Primary_Completion_Rate"

regs = regions.build()
csl = ISO_countries.build()
sp_chars = special_chars.build()

mappings = [ 'Country_Name', 'Survey_Name', 
              CWS+'_:_Year', CWS+'_:_Survey_Source', CWS+'_:_Age_Range', CWS +'_:_Total_Child_Population',
              CWS+'_:_Total_Percentage_of_Working_Children', CWS+'_:_Total_Working_Population', 
              CWS+'_:_Agriculture', CWS+'_:_Service', CWS+'_:_Industry', 
              ESAS+'_:_Year', ESAS+'_:_Age_Range', ESAS+'_:_Percentage', 
              CWAS+'_:_Year', CWAS+'_:_Age_Range', CWAS+'_:_Total', 
              UPCR+'_:_Year', UPCR+'_:_Rate' 
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
	    md[CWS+'_:_Year'] = mdrec[CWS+'_:_Year']
	    md[CWS+'_:_Survey_Source'] = mdrec[CWS+'_:_Survey_Source']
	    md[CWS+'_:_Age_Range'] = mdrec[CWS+'_:_Age_Range']
	    md[CWS +'_:_Total_Child_Population'] = mdrec[CWS +'_:_Total_Child_Population']
	    md[CWS+'_:_Total_Percentage_of_Working_Children'] = mdrec[CWS+'_:_Total_Percentage_of_Working_Children']
	    md[CWS+'_:_Total_Working_Population'] = mdrec[CWS+'_:_Total_Working_Population']
	    md[CWS+'_:_Agriculture'] = mdrec[CWS+'_:_Agriculture']
	    md[CWS+'_:_Service'] = mdrec[CWS+'_:_Service']
	    md[CWS+'_:_Industry'] = mdrec[CWS+'_:_Industry']
	    md[ESAS+'_:_Year'] = mdrec[ESAS+'_:_Year']
	    md[ESAS+'_:_Age_Range'] = mdrec[ESAS+'_:_Age_Range']
	    md[ESAS+'_:_Percentage'] = mdrec[ESAS+'_:_Percentage']
	    md[CWAS+'_:_Year'] = mdrec[CWAS+'_:_Year']
	    md[CWAS+'_:_Age_Range'] = mdrec[CWAS+'_:_Age_Range']
	    md[CWAS+'_:_Total'] = mdrec[CWAS+'_:_Total']
	    md[UPCR+'_:_Year'] = mdrec[UPCR+'_:_Year']
	    md[UPCR+'_:_Rate'] = mdrec[UPCR+'_:_Rate']
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
	target.write(md[CWS+'_:_Year'])
	target.write("</Year>\n")
	target.write("\t\t\t<Survey_Score>")
	target.write(md[CWS+'_:_Survey_Source'])
	target.write("</Survey_Score>\n")
	target.write("\t\t\t<Age_Range>")
	target.write(md[CWS+'_:_Age_Range'])
	target.write("</Age_Range>\n")
	target.write("\t\t\t<Total_Child_Population>")
	target.write(md[CWS +'_:_Total_Child_Population'])
	target.write("\t\t\t</Total_Child_Population>\n")
	target.write("\t\t\t<Total_Percentage_of_Working_Children>")
	target.write(str(md[CWS+'_:_Total_Percentage_of_Working_Children']))
	target.write("</Total_Percentage_of_Working_Children>\n")
	target.write("\t\t\t<Total_Working_Population>")
	target.write(str(md[CWS+'_:_Total_Working_Population']))
	target.write("</Total_Working_Population>\n")
	target.write("\t\t\t<Agriculture>")
	target.write(str(md[CWS+'_:_Agriculture']))
	target.write("</Agriculture>\n")
	target.write("\t\t\t<Service>")
	target.write(str(md[CWS+'_:_Service']))
	target.write("</Service>\n")
	target.write("\t\t\t<Industry>")
	target.write(str(md[CWS+'_:_Industry']))
	target.write("</Industry>\n")
	target.write("\t\t</Childrens_Work_Statistics>\n")
	
	target.write("\t\t<Education_Statistics_Attendance_Statistics>\n")
	target.write("\t\t\t<Year>")
	target.write(md[ESAS+'_:_Year'])
	target.write("</Year>\n")
	target.write("\t\t\t<Age_Range>")
	target.write(md[ESAS+'_:_Age_Range'])
	target.write("</Age_Range>\n")
	target.write("\t\t\t<Percentage>")
	target.write(md[ESAS+'_:_Percentage'])
	target.write("</Percentage>\n")
	target.write("\t\t</Education_Statistics_Attendance_Statistics>\n")

	target.write("\t\t<Children_Work_And_Studying>\n")
	target.write("\t\t\t<Year>")
	target.write(md[CWAS+'_:_Year'])
	target.write("</Year>\n")
	target.write("\t\t\t<Age_Range>")
	target.write(md[CWAS+'_:_Age_Range'])
	target.write("</Age_Range>\n")
	target.write("\t\t\t<Total>")
	target.write(md[CWAS+'_:_Total'])
	target.write("</Total>\n")
	target.write("\t\t</Children_Work_And_Studying>\n")

	target.write("\t\t<Unesco_Primary_Completion_Rate>\n")
	target.write("\t\t\t<Year>")
	target.write(md[UPCR+'_:_Year'])
	target.write("</Year>\n")
	target.write("\t\t\t<Rate>")
	target.write(md[UPCR+'_:_Rate'])
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
		newcws['Year'] = mdrec[CWS+'_:_Year']
		newcws['Survey_Source'] = mdrec[CWS+'_:_Survey_Source']
		newcws['Age_Range'] = mdrec[CWS+'_:_Age_Range']
		newcws['Total_Child_Population'] = mdrec[CWS +'_:_Total_Child_Population']
		newcws['Total_Percentage_of_Working_Children'] = mdrec[CWS+'_:_Total_Percentage_of_Working_Children']
		newcws['Total_Working_Population'] = mdrec[CWS+'_:_Total_Working_Population']
		newcws['Agriculture'] = mdrec[CWS+'_:_Agriculture']
		newcws['Service'] = mdrec[CWS+'_:_Service']
		newcws['Industry'] = mdrec[CWS+'_:_Industry']
		md[CWS].append(newcws)

		md[ESAS] = []
		newesas = OrderedDict()
		newesas['Year'] = mdrec[ESAS+'_:_Year']
		newesas['Age Range'] = mdrec[ESAS+'_:_Age_Range']
		newesas['Percentage'] = mdrec[ESAS+'_:_Percentage']
		md[ESAS].append(newesas)

		md[CWAS] = []
		newcwas = OrderedDict()
		newcwas['Year'] = mdrec[CWAS+'_:_Year']
		newcwas['Age Range'] = mdrec[CWAS+'_:_Age_Range']
		newcwas['Total'] = mdrec[CWAS+'_:_Total']
		md[CWAS].append(newcwas)

		md[UPCR] = []
		newupcr = OrderedDict()
		newupcr['Year'] = mdrec[UPCR+'_:_Year']
		newupcr['Rate'] = mdrec[UPCR+'_:_Rate']
		md[UPCR].append(newupcr)
		result.append(md)

	return result

if __name__ == '__main__':
	
	mdlist = build()

	to_xml(xml_target, mdlist)
	to_json(json_target, mdlist)
	to_csv(csv_target, mdlist)

	