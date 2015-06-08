

import utility
import regions
from collections import OrderedDict

csv_target = '../output/extra/master_data_from_XL_2013.csv' 
xml_target = '../output/extra/master_data_from_XL_2013.xml' 
json_target = '../output/extra/master_data_from_XL_2013.json' 

regs = regions.build()

mappings = [ "Country_Name", "Country_Region", "Assessment",
             "C. 138 Ratified" ,"C. 138 Ratified during Reporting Period",
             "C. 182 Ratified","C. 182 Ratified during Reporting Period",
             "Convention on the Rights of the Child (CRC) Ratified",
             "Convention on the Rights of the Child (CRC) Ratified during Reporting Period",
             "CRC - Commercial Sexual Exploitation of Children (CSEC) Ratified",
             "CRC-CSEC Ratified during Reporting Period",
             "CRC - Armed Conflict (AC)  Ratified",
             "CRC - AC Ratified during Reporting Period",
             "Palermo Ratified","Palermo Ratified during reporting period",
             "Minimum Age for Work Established",
             "Minimum Age for Work Established or Amended during Reporting Period",
             "Minimum Age Conforms to International Standards",
             "Minimum Age for Work","Minimum Age for Hazardous Work Established",
             "Minimum Age for Hazardous Work Established or Amended during Reporting Period",
             "Minimum Age for Hazardous Work Conforms to International Standards","Minimum Age for Hazardous Work",
             "Compulsory Education Age Established",
             "Compulsory Education Age Established or Amended during Reporting Period",
             "Minimum Age for Compulsory Education Conforms to International Standards",
             "Minimum Age for Compulsory Education",
             "Free Public Education Established",
             "Free Public Education Established or Amended during Reporting Period",
             "Country has Mechanism to Coordinate its Efforts in Combatting the WFCL",
             "Country Established or Amended Mechanism to Coordinate during Reporting Period",
             "National Policy on WFCL Established",
             "National Policy of WFCL Established or Amended during Reporting Period",
             "Country Made at least one Effort to Advance the Elimination of the Worst Forms of Child Labor",
             "Country made at least one Effort to Change Laws and Regulations",
             "Country Made at least one Enforcement Effort",
             "Country made at least one Coordination Effort",
             "Country made at least one Policy Effort",
             "Country made at least one Social Program Effort"
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
			valuetext = str(country_record[currentkey])
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
