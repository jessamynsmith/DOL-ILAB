

import xlrd
from collections import OrderedDict
 
source_filename = '../source_data/Master_Data_Table_for_TDA2014_30_jan_2015.xlsx' 

xml_header = """<?xml version="1.0" encoding="UTF-8"?>"""

CWS = '''Children's Work Statistics'''
ESAS = "Education Statistics: Attendance Statistics"
CWAS = "Children Working and Studying (7-14 yrs old)"
UPCR = "UNESCO Primary Completion Rate"


def get_master_data_from_excel():
	# Open the workbook and select the first worksheet
	wb = xlrd.open_workbook(source_filename)
	sh = wb.sheet_by_index(0)
	md_list = []
	# Iterate through each row in worksheet 
	for rownum in range(3, sh.nrows):
	    md = OrderedDict()
	    row_values = sh.row_values(rownum)
	    md['Year'] = row_values[0]
	    md['Country'] = str(row_values[1]).strip()
	    md['Survey Name'] = row_values[2]
	    md[CWS+' : Year'] = str(row_values[3]).strip()
	    md[CWS+' : Survey Source'] = str(row_values[4]).strip()
	    md[CWS+' : Age Range'] = str(row_values[5]).strip()
	    md[CWS+' : Total Child Population'] = row_values[6]
	    md[CWS+' : Total % of Working Children'] = row_values[7]
	    md[CWS+' : Total Working Population'] = row_values[8]
	    md[CWS+' : Agriculture'] = row_values[9]
	    md[CWS+' : Service'] = row_values[10]
	    md[CWS+' : Industry'] = row_values[11]
	    md[ESAS+' : Year'] = row_values[12]
	    md[ESAS+' : Age Range'] = str(row_values[13]).strip()
	    md[ESAS+' : %'] = row_values[14]
	    md[CWAS+' : Year'] = str(row_values[15]).strip()
	    md[CWAS+' : Age Range'] = str(row_values[16]).strip()
	    md[CWAS+' : Total'] = row_values[17]
	    md[UPCR+' : Year'] = row_values[18]
	    md[UPCR+' : Rate'] = row_values[19]
	    md_list.append(md)
	    #print str(rownum)
	    #print md
	return md_list

def write_record(target, md):

	#print md, "\n"

	target.write("\t\t<Country>\n")

	target.write("\t\t\t<Name>")
	target.write(md['Country'])
	target.write("</Name>\n")

	target.write("\t\t\t<Survey_Name>")
	target.write((md['Survey Name']).encode('utf8') )
	target.write("</Survey_Name>\n")

	target.write("\t\t\t<Childrens_Work_Statistics>\n")
	target.write("\t\t\t\t<Year>")
	target.write(md[CWS+' : Year'])
	target.write("</Year>\n")
	target.write("\t\t\t\t<Survey_Score>")
	target.write(md[CWS+' : Survey Source'])
	target.write("</Survey_Score>\n")
	target.write("\t\t\t\t<Age_Range>")
	target.write(md[CWS+' : Age Range'])
	target.write("</Age_Range>\n")
	target.write("\t\t\t\t<Total_Child_Population>")
	target.write(str(md[CWS+' : Total Child Population']))
	target.write("</Total_Child_Population>\n")
	target.write("\t\t\t\t<Total_Percentage_of_Working_Children>")
	target.write(str(md[CWS+' : Total % of Working Children']))
	target.write("</Total_Percentage_of_Working_Children>\n")
	target.write("\t\t\t\t<Total_Working_Population>")
	target.write(str(md[CWS+' : Total Working Population']))
	target.write("</Total_Working_Population>\n")
	target.write("\t\t\t\t<Agriculture>")
	target.write(str(md[CWS+' : Agriculture']))
	target.write("</Agriculture>\n")
	target.write("\t\t\t\t<Service>")
	target.write(str(md[CWS+' : Service']))
	target.write("</Service>\n")
	target.write("\t\t\t\t<Industry>")
	target.write(str(md[CWS+' : Industry']))
	target.write("</Industry>\n")
	target.write("\t\t\t</Childrens_Work_Statistics>\n")

	target.write("\t\t\t<Education_Statistics_Attendance_Statistics>\n")
	target.write("\t\t\t\t<Year>")
	md[ESAS+' : Year']
	target.write("</Year>\n")
	target.write("\t\t\t\t<Age_Range>")
	md[ESAS+' : Age Range']
	target.write("</Age_Range>\n")
	target.write("\t\t\t\t<Percentage>")
	md[ESAS+' : %']
	target.write("</Percentage>\n")
	target.write("\t\t\t</Education_Statistics_Attendance_Statistics>\n")

	target.write("\t\t\t<Children_Work_And_Studying>\n")
	target.write("\t\t\t\t<Year>")
	md[CWAS+' : Year']
	target.write("</Year>\n")
	target.write("\t\t\t\t<Age_Range>")
	md[CWAS+' : Age Range']
	target.write("</Age_Range>\n")
	target.write("\t\t\t\t<Total>")
	md[CWAS+' : Total']
	target.write("</Total>\n")
	target.write("\t\t\t</Children_Work_And_Studying>\n")

	target.write("\t\t\t<Unesco_Primary_Completion_Rate>\n")
	target.write("\t\t\t\t<Year>")
	md[UPCR+' : Year']
	target.write("</Year>\n")
	target.write("\t\t\t\t<Rate>")
	md[UPCR+' : Rate']
	target.write("</Rate>\n")
	target.write("\t\t\t</Unesco_Primary_Completion_Rate>\n")

	target.write("\t\t</Country>\n")


	return

def xml_master_data(mlist, filename):

	target = open(filename, 'w+')

	# Write XML Header
	target.write(xml_header+"\n")
	target.write("<Master_Data>\n")
	
	yr = []
	n = 0

	for country_record in mlist:
		year = country_record['Year']
		n = n+1
		if (year not in yr):
			if (len(yr) > 0) and (n != (len(mlist))):
				target.write("\t</Year>\n")
			target.write("\t"+"<Year>"+"\n"+"\t\t<Year_Name>"+str(int(year))+"</Year_Name>"+"\n")
			yr.append(year)
		write_record(target, country_record)
	target.write("\t</Year>\n")
	target.write("</Master_Data>\n")
	target.close()

	return

if __name__ == '__main__':
	
	mdlist = get_master_data_from_excel()
	#print mdlist
	
	xml_master_data(mdlist, "../output/master_data_by_country.xml")

