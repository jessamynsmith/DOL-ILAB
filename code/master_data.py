

import utility
import regions
import special_chars
from collections import OrderedDict

csv_target = '../output/extra/master_data_from_XL_2013.csv' 
xml_target = '../output/extra/master_data_from_XL_2013.xml' 
json_target = '../output/extra/master_data_from_XL_2013.json' 

regs = regions.build()
sp_chars = special_chars.build()

mappings = [ "Country_Name", "Country_Region", "Assessment",
             "C_138_Ratified" ,"C_138_Ratified_during_Reporting_Period",
             "C_182_Ratified","C_182_Ratified_during_Reporting_Period",
             "Convention_on_the_Rights_of_the_Child_Ratified",
             "Convention_on_the_Rights_of_the_Child_Ratified_during_Reporting_Period",
             "CRC_Commercial_Sexual_Exploitation_of_Children_Ratified",
             "CRC_CSEC_Ratified_during_Reporting_Period",
             "CRC_Armed_Conflict_Ratified",
             "CRC_AC_Ratified_during_Reporting_Period",
             "Palermo_Ratified","Palermo_Ratified_during_reporting_period",
             "Minimum_Age_for_Work_Established",
             "Minimum_Age_for_Work_Established_or_Amended_during_Reporting_Period",
             "Minimum_Age_Conforms_to_International_Standards",
             "Minimum_Age_for_Work","Minimum_Age_for_Hazardous_Work_Established",
             "Minimum_Age_for_Hazardous_Work_Established_or_Amended_during_Reporting_Period",
             "Minimum_Age_for_Hazardous_Work_Conforms_to_International_Standards","Minimum_Age_for_Hazardous_Work",
             "Compulsory_Education_Age_Established",
             "Compulsory_Education_Age_Established_or_Amended_during_Reporting_Period",
             "Minimum_Age_for_Compulsory_Education_Conforms_to_International_Standards",
             "Minimum_Age_for_Compulsory_Education",
             "Free_Public_Education_Established",
             "Free_Public_Education_Established_or_Amended_during_Reporting_Period",
             "Country_has_Mechanism_to_Coordinate_its_Efforts_in_Combatting_the_WFCL",
             "Country_Established_or_Amended_Mechanism_to_Coordinate_during_Reporting_Period",
             "National_Policy_on_WFCL_Established",
             "National_Policy_on_WFCL_Established_or_Amended_during_Reporting_Period"
             ]


def build():
	master_data = utility.from_excelsheet(utility.get_source_filename(), 4, 1, mappings)
	results = include_extra(master_data)
	return results

def include_extra(masterdata):
	md_list = []
	for mdrec in masterdata:
	    md = OrderedDict()
	    md['Country_Name'] = mdrec['Country_Name']
	    md['Country_ISO2'] = regions.find_ISO2_from_name(md['Country_Name'], regs)
	    md['Country_ISO3'] = regions.find_ISO3_from_name(md['Country_Name'], regs)
	    md['Country_Region'] = regions.find_region_from_name(md['Country_Name'], regs)
	    mdreckeys = mdrec.keys()
	    for n in range(2, len(mdrec)):
	    	currentkey = mdreckeys[n]
	    	md[currentkey] = mdrec[currentkey]
	    md_list.append(md)
	return md_list


def to_xml(filename, mlist):
	target = open(filename, 'w+')
	target.write(utility.get_xml_header()+"\n")
	target.write("<Master_Data>\n")
	for country_record in mlist:
		target.write("\t<Country>\n")
		mkeys = country_record.keys()
		for n in range(0, len(mkeys)):
			currentkey = mkeys[n]
			opentext = "\t\t<"+ currentkey +">"
			valuetext = special_chars.xml_safe(str(country_record[currentkey]),sp_chars)
			closetext = "</" + currentkey +">\n"
			target.write(opentext+valuetext+closetext)
		target.write("\t</Country>\n")
	target.write("</Master_Data>\n")
	target.close()
	return

def to_json(filename, data):
	utility.to_json(filename, data)
	return

def to_csv(filename, data):
	utility.to_csv_from_OD(filename, data)
	return

if __name__ == '__main__':
	
	mdlist = build()

	to_xml(xml_target, mdlist)
	to_json(json_target, mdlist)
	to_csv(csv_target, mdlist)
