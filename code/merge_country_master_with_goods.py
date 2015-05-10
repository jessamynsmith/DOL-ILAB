from collections import OrderedDict
import generate_master_data, add_iso2_to_goods_and_products

xml_header = """<?xml version="1.0" encoding="UTF-8"?>"""

CWS = '''Children's Work Statistics'''
ESAS = "Education Statistics: Attendance Statistics"
CWAS = "Children Working and Studying (7-14 yrs old)"
UPCR = "UNESCO Primary Completion Rate"


def get_good_set(goods, year, iso2):

	outer = []

	if iso2 != -1:
		for n in range(0, len(goods)):
			inner = []
			if (goods[n]['Year'] == int(year)) and (goods[n]['ISO2'].strip() == iso2.strip()):
				inner.append(goods[n]['Good'])
				inner.append(goods[n]['Child Labor'])
				inner.append(goods[n]['Forced Labor'])
				inner.append(goods[n]['Forced Child Labor'])
				outer.append(inner)
	
	return outer



def master_with_all_goods(mdlist, goods):

	outlist = []

	for m in mdlist:
		md = OrderedDict()
		md['Year'] = m['Year']
		md['Country'] = m['Country']
		md['ISO2'] = add_iso2_to_goods_and_products.get_ISO2(md['Country'])
		if md['ISO2'] == -1:
			print "ISO2 code not found for", md['Country']
		md['Goods'] = get_good_set(goods, md['Year'], md['ISO2'])
		md['Survey Name'] = m['Survey Name']
		md[CWS+' : Year'] = m[CWS+' : Year']
		md[CWS+' : Survey Source'] = m[CWS+' : Survey Source']
		md[CWS+' : Age Range'] = m[CWS+' : Age Range']
		md[CWS+' : Total Child Population'] = m[CWS+' : Total Child Population']
		md[CWS+' : Total % of Working Children'] = m[CWS+' : Total % of Working Children']
		md[CWS+' : Total Working Population'] = m[CWS+' : Total Working Population']
		md[CWS+' : Agriculture'] = m[CWS+' : Agriculture']
		md[CWS+' : Service'] = m[CWS+' : Service']
		md[CWS+' : Industry'] = m[CWS+' : Industry']
		md[ESAS+' : Year'] = m[ESAS+' : Year']
		md[ESAS+' : Age Range'] = m[ESAS+' : Age Range']
		md[ESAS+' : %'] = m[ESAS+' : %']
		md[CWAS+' : Year'] = m[CWAS+' : Year']
		md[CWAS+' : Age Range'] = m[CWAS+' : Age Range']
		md[CWAS+' : Total'] = m[CWAS+' : Total']
		md[UPCR+' : Year'] = m[UPCR+' : Year']
		md[UPCR+' : Rate'] = m[UPCR+' : Rate']
		outlist.append(md)

	return outlist


def write_record(target, md):

	#print md, "\n"

	target.write("\t\t<Country>\n")

	target.write("\t\t\t<Name>")
	target.write(md['Country'])
	target.write("</Name>\n")

	target.write("\t\t\t<ISO2>")
	target.write(md['ISO2'])
	target.write("</ISO2>\n")

	goods = md['Goods']

	target.write("\t\t\t<Good_List>\n")

	for good in goods:
		target.write("\t\t\t\t<Good>\n")
		target.write("\t\t\t\t\t<Good_Name>")
		target.write(good[0].strip())
		target.write("</Good_Name>\n")
		target.write("\t\t\t\t\t<Child_Labor>")
		target.write(good[1].strip())
		target.write("</Child_Labor>\n")	
		target.write("\t\t\t\t\t<Forced_Labor>")
		target.write(good[2].strip())
		target.write("</Forced_Labor>\n")	
		target.write("\t\t\t\t\t<Forced_Child_Labor>")
		target.write(good[3].strip())
		target.write("</Forced_Child_Labor>\n")	
		target.write("\t\t\t\t</Good>\n")

	target.write("\t\t\t</Good_List>\n")		

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


def to_xml(mlist, filename):

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


def build():

	mdb = generate_master_data.build()
	gdb = add_iso2_to_goods_and_products.build()

	mdgd = master_with_all_goods(mdb, gdb)

	return mdgd



if __name__ == '__main__':  

	newm = build()

	to_xml(newm, "../output/extra/master_data_ISO_2013_by_country.xml")





