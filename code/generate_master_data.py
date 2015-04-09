

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
	    md['Country'] = str(row_values[0]).strip()
	    md['Survey Name'] = row_values[1]
	    md[CWS+' : Year'] = str(row_values[2]).strip()
	    md[CWS+' : Survey Source'] = str(row_values[3]).strip()
	    md[CWS+' : Age Range'] = str(row_values[4]).strip()
	    md[CWS+' : Total Child Population'] = row_values[5]
	    md[CWS+' : Total % of Working Children'] = row_values[6]
	    md[CWS+' : Total Working Population'] = row_values[7]
	    md[CWS+' : Agriculture'] = row_values[8]
	    md[CWS+' : Service'] = row_values[9]
	    md[CWS+' : Industry'] = row_values[10]
	    md[ESAS+' : Year'] = row_values[11]
	    md[ESAS+' : Age Range'] = str(row_values[12]).strip()
	    md[ESAS+' : %'] = row_values[13]
	    md[CWAS+' : Year'] = str(row_values[14]).strip()
	    md[CWAS+' : Age Range'] = str(row_values[15]).strip()
	    md[CWAS+' : Total'] = row_values[16]
	    md[UPCR+' : Year'] = row_values[17]
	    md[UPCR+' : Rate'] = row_values[18]
	    md_list.append(md)
	    print str(rownum)
	    print md
	return md_list


if __name__ == '__main__':
	mdlist = get_master_data_from_excel()
	#print mdlist

