import xlrd
from collections import OrderedDict
import add_iso2_to_goods_and_products

source_filename = '../source_data/TDA_Structured_Data_Country_Region.xlsx' 
xml_header = """<?xml version="1.0" encoding="UTF-8"?>"""

def from_excelsheet(sheetno):
	# Open the workbook and select the first worksheet
	wb = xlrd.open_workbook(source_filename)
	sh = wb.sheet_by_index(sheetno)
	rows = []
	# Iterate through each row in worksheet 
	for rownum in range(1, sh.nrows):
	    row = OrderedDict()
	    row_values = sh.row_values(rownum)
	    row['Region'] = row_values[0]
	    row['Country'] = row_values[1]
	    rows.append(row)
	return rows

def include_ISO(rlist):
	result = []

	for r in rlist:
		row = OrderedDict()
		row['Region'] = r['Region']
		row['Country'] = r['Country']
		cn = r['Country'].encode('utf-8')
		row['ISO2'] = add_iso2_to_goods_and_products.get_ISO2(cn)
		result.append(row)
	return result

def build():
	regs = from_excelsheet(0)
	results = include_ISO(regs)
	return results

def find_by_name(cn, reglist):
	result = -1
	for reg in reglist:
		if (reg['Country'].encode('utf-8').upper().strip() == cn.upper().strip()):
			result = reg['Region']
			break
	return result

def find_by_ISO2(i2, reglist):
	result = -1
	for reg in reglist:
		if (reg['ISO2'].upper().strip() == i2.upper().strip()):
			result = reg['Region']
			break
	return result

def get_region_from_name(cname):
	result = -1
	res = build()
	result = find_by_name(cname, res)
	return result

def get_region_from_ISO2(iso2):
	result = -1
	res = build()
	result = find_by_ISO2(iso2, res)
	return result

if __name__ == '__main__':
	regions = build()

	print get_region_from_ISO2("JM")

	print get_region_from_name("Argentina")