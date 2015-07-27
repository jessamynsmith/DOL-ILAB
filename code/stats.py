

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

mappings = [ 'Country_Name', 
              CWS+'_Age_Range', CWS+'_Total_Percentage_of_Working_Children',
              CWS+'_Total_Working_Population', 
              CWS+'_Agriculture', CWS+'_Services', CWS+'_Industry', 
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
	    md[CWS+'_Age_Range'] = mdrec[CWS+'_Age_Range']
	    md[CWS+'_Total_Percentage_of_Working_Children'] = mdrec[CWS+'_Total_Percentage_of_Working_Children']
	    md[CWS+'_Total_Working_Population'] = mdrec[CWS+'_Total_Working_Population']
	    md[CWS+'_Agriculture'] = mdrec[CWS+'_Agriculture']
	    md[CWS+'_Services'] = mdrec[CWS+'_Services']
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

	target.write(utility.tabs(2)+"<Country_Name>")
	target.write(md['Country_Name'])
	target.write("</Country_Name>"+utility.get_newline())

	target.write(utility.tabs(2)+"<Country_ISO2>")
	target.write(str(md['Country_ISO2']))
	target.write("</Country_ISO2>"+utility.get_newline())

	target.write(utility.tabs(2)+"<Country_ISO3>")
	target.write(str(md['Country_ISO3']))
	target.write("</Country_ISO3>"+utility.get_newline())

	target.write(utility.tabs(2)+"<Country_Region>")
	target.write(special_chars.xml_safe(str(md['Country_Region']),sp_chars))
	target.write("</Country_Region>"+utility.get_newline())
	return


def write_data(target, md, count):
	target.write(utility.tabs(count)+"<Childrens_Work_Statistics>"+utility.get_newline())
	target.write(utility.tabs(count+1)+"<Age_Range>")
	target.write(md[CWS+'_Age_Range'])
	target.write("</Age_Range>"+utility.get_newline())
	target.write(utility.tabs(count+1)+"<Total_Percentage_of_Working_Children>")
	target.write(str(md[CWS+'_Total_Percentage_of_Working_Children']))
	target.write("</Total_Percentage_of_Working_Children>"+utility.get_newline())
	target.write(utility.tabs(count+1)+"<Total_Working_Population>")
	target.write(str(md[CWS+'_Total_Working_Population']))
	target.write("</Total_Working_Population>"+utility.get_newline())
	target.write(utility.tabs(count+1)+"<Agriculture>")
	target.write(str(md[CWS+'_Agriculture']))
	target.write("</Agriculture>"+utility.get_newline())
	target.write(utility.tabs(count+1)+"<Services>")
	target.write(str(md[CWS+'_Services']))
	target.write("</Services>"+utility.get_newline())
	target.write(utility.tabs(count+1)+"<Industry>")
	target.write(str(md[CWS+'_Industry']))
	target.write("</Industry>"+utility.get_newline())
	target.write(utility.tabs(count)+"</Childrens_Work_Statistics>"+utility.get_newline())
	
	target.write(utility.tabs(count)+"<Education_Statistics_Attendance_Statistics>"+utility.get_newline())
	target.write(utility.tabs(count+1)+"<Year>")
	target.write(md[ESAS+'_Year'])
	target.write("</Year>"+utility.get_newline())
	target.write(utility.tabs(count+1)+"<Age_Range>")
	target.write(md[ESAS+'_Age_Range'])
	target.write("</Age_Range>"+utility.get_newline())
	target.write(utility.tabs(count+1)+"<Percentage>")
	target.write(md[ESAS+'_Percentage'])
	target.write("</Percentage>"+utility.get_newline())
	target.write(utility.tabs(count)+"</Education_Statistics_Attendance_Statistics>"+utility.get_newline())

	target.write(utility.tabs(count)+"<Children_Work_And_Studying>"+utility.get_newline())
	target.write(utility.tabs(count+1)+"<Year>")
	target.write(md[CWAS+'_Year'])
	target.write("</Year>"+utility.get_newline())
	target.write(utility.tabs(count+1)+"<Age_Range>")
	target.write(md[CWAS+'_Age_Range'])
	target.write("</Age_Range>"+utility.get_newline())
	target.write(utility.tabs(count+1)+"<Total>")
	target.write(md[CWAS+'_Total'])
	target.write("</Total>"+utility.get_newline())
	target.write(utility.tabs(count)+"</Children_Work_And_Studying>"+utility.get_newline())

	target.write(utility.tabs(count)+"<Unesco_Primary_Completion_Rate>"+utility.get_newline())
	target.write(utility.tabs(count+1)+"<Year>")
	target.write(md[UPCR+'_Year'])
	target.write("</Year>"+utility.get_newline())
	target.write(utility.tabs(count+1)+"<Rate>")
	target.write(md[UPCR+'_Rate'])
	target.write("</Rate>"+utility.get_newline())
	target.write(utility.tabs(count)+"</Unesco_Primary_Completion_Rate>"+utility.get_newline())
	return

def to_xml(filename, mlist):
	target = open(filename, 'w+')
	target.write(utility.get_xml_header()+""+utility.get_newline())
	target.write("<Country_Statistics>"+utility.get_newline())
	for country_record in mlist:
		target.write(utility.tabs(1)+"<Country>"+utility.get_newline())
		write_record(target, country_record)
		write_data(target, country_record, 2)
		target.write(utility.tabs(1)+"</Country>"+utility.get_newline())		
	target.write("</Country_Statistics>"+utility.get_newline())
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
		md[CWS] = []

		newcws = OrderedDict()
		newcws['Age_Range'] = mdrec[CWS+'_Age_Range']
		newcws['Total_Percentage_of_Working_Children'] = mdrec[CWS+'_Total_Percentage_of_Working_Children']
		newcws['Total_Working_Population'] = mdrec[CWS+'_Total_Working_Population']
		newcws['Agriculture'] = mdrec[CWS+'_Agriculture']
		newcws['Services'] = mdrec[CWS+'_Services']
		newcws['Industry'] = mdrec[CWS+'_Industry']
		md[CWS].append(newcws)

		md[ESAS] = []
		newesas = OrderedDict()
		newesas['Year'] = mdrec[ESAS+'_Year']
		newesas['Age_Range'] = mdrec[ESAS+'_Age_Range']
		newesas['Percentage'] = mdrec[ESAS+'_Percentage']
		md[ESAS].append(newesas)

		md[CWAS] = []
		newcwas = OrderedDict()
		newcwas['Year'] = mdrec[CWAS+'_Year']
		newcwas['Age_Range'] = mdrec[CWAS+'_Age_Range']
		newcwas['Total'] = mdrec[CWAS+'_Total']
		md[CWAS].append(newcwas)

		md[UPCR] = []
		newupcr = OrderedDict()
		newupcr['Year'] = mdrec[UPCR+'_Year']
		newupcr['Rate'] = mdrec[UPCR+'_Rate']
		md[UPCR].append(newupcr)
		result.append(md)

	return result

def found_stats_from(value, tag, mlist):
	found = utility.get_default_error()

	for count in range(0, len(mlist)):
		stat = mlist[count]
		if (stat[tag].strip().upper() == value.strip().upper()) :
			found = count
			break
	return found


def get_stats_from_iso3(iso3, mlist):

	stats = utility.get_default_error()
	index = found_stats_from(iso3, "Country_ISO3", mlist)

	if index != utility.get_default_error() :
		print "found"
		stats = mlist[index]
	else:
		print "not found"

	return stats


def get_stats_from_name(name, mlist):
	this_iso3 = ISO_countries.ISO3_from_name(name, csl)
	stats = get_stats_from_iso3(this_iso3, mlist)
	return stats

def country_with_no_stats(mdlist, regs):
	tab4 = utility.grab_values_for_tag(mdlist, "Country_Name")
	tab1 = utility.grab_values_for_tag(regs, "Country_Name")
	diff = utility.set_difference(tab1, tab4)
	return diff

if __name__ == '__main__':
	
	mdlist = build()

	to_xml(xml_target, mdlist)
	to_json(json_target, mdlist)
	to_csv(csv_target, mdlist)
     
	#print get_stats_from_name("Cambodia", mdlist)

	tab4 = utility.grab_values_for_tag(mdlist, "Country_Name")
	tab1 = utility.grab_values_for_tag(regs, "Country_Name")
	diff = utility.set_difference(tab1, tab4)

	print "\n\nCountries with no stats: ", diff
	

	