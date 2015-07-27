

import utility
import regions
import special_chars
import ISO_countries
from collections import OrderedDict

csv_target = '../output/extra/master_data_from_XL_2013.csv' 
xml_target = '../output/extra/master_data_from_XL_2013.xml' 
json_target = '../output/extra/master_data_from_XL_2013.json' 

regs = regions.build()
csl = ISO_countries.build()
sp_chars = special_chars.build()

mappings = [ "Country_Name", "Country_Region", "Assessment",
             "C_138_Ratified" , "C_182_Ratified",
             "Convention_on_the_Rights_of_the_Child_Ratified",
             "CRC_Commercial_Sexual_Exploitation_of_Children_Ratified",
             "CRC_Armed_Conflict_Ratified",
             "Palermo_Ratified",
             "Minimum_Age_for_Work_Estabslished",
             "Minimum_Age_for_Work",
             "Minimum_Age_for_Hazardous_Work_Estabslished",
             "Minimum_Age_for_Hazardous_Work",
             "Compulsory_Education_Age_Estabslished",
             "Minimum_Age_for_Compulsory_Education",
             "Free_Public_Education_Estabslished",
             "Country_has_Mechanism_to_Coordinate_its_Efforts_in_Combatting_the_WFCL",
             "National_Policy_on_WFCL_Estabslished"
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
	    md['Country_ISO2'] = str(ISO_countries.ISO2_from_name(md['Country_Name'], csl))
	    md['Country_ISO3'] = str(ISO_countries.ISO3_from_name(md['Country_Name'], csl))
	    md['Country_Region'] = str(regions.find_region_from_ISO3(md['Country_ISO3'], regs))
	    mdreckeys = mdrec.keys()
	    for n in range(2, len(mdrec)):
	    	currentkey = mdreckeys[n]
	    	md[currentkey] = mdrec[currentkey]
	    md_list.append(md)
        if (md['Country_ISO2'] == "-1"):
            print " No ISO2 code found for ", md['Country_Name']
        if (md['Country_ISO3'] == "-1"):
            print " No ISO3 code found for ", md['Country_Name']            
        if (mdrec['Country_Region'].strip().upper() != md['Country_Region'].strip().upper()):
            print "Region mismatch between region information in Tab 5 and Tab 1 for ", mdrec['Country_Name']

	return md_list


def to_xml(filename, mlist):
    target = open(filename, 'w+')
    target.write(utility.get_xml_header()+utility.get_newline())
    target.write("<Country_Master_Data>"+utility.get_newline())
    for country_record in mlist:
        target.write(utility.tabs(1)+"<Country>"+utility.get_newline())
        write_front(target, country_record, 2)
        write_rest(target, country_record, 2)
        target.write(utility.tabs(1)+"</Country>"+utility.get_newline())
    target.write("</Country_Master_Data>"+utility.get_newline())
    target.close()
    return

def write_front(target, country_record, count):
    target.write(utility.tabs(count)+"<Country_Name>"+country_record["Country_Name"]+"</Country_Name>"+utility.get_newline())
    target.write(utility.tabs(count)+"<Country_ISO2>"+country_record["Country_ISO2"]+"</Country_ISO2>"+utility.get_newline())
    target.write(utility.tabs(count)+"<Country_ISO3>"+country_record["Country_ISO3"]+"</Country_ISO3>"+utility.get_newline())
    target.write(utility.tabs(count)+"<Country_Region>"+special_chars.xml_safe(country_record["Country_Region"], sp_chars)+"</Country_Region>"+utility.get_newline())
    target.write(utility.tabs(count)+"<Assessment>"+country_record["Assessment"]+"</Assessment>"+utility.get_newline())
    return
    
def write_rest(target, country_record, count):
    mkeys = country_record.keys()
    for n in range(5, len(mkeys)):
        currentkey = mkeys[n]
        opentext = utility.tabs(count)+"<"+ currentkey +">"
        valuetext = special_chars.xml_safe(str(country_record[currentkey]),sp_chars)
        closetext = "</" + currentkey +">"+utility.get_newline()
        target.write(opentext+valuetext+closetext)
    return

def found_master_data_from(value, tag, mlist):
    found = utility.get_default_error()

    for count in range(0, len(mlist)):
        md = mlist[count]
        if (md[tag].strip().upper() == value.strip().upper()) :
            found = count
            break
    return found


def get_master_data_from_iso3(iso3, mlist):
    md = utility.get_default_error()
    index = found_master_data_from(iso3, "Country_ISO3", mlist)
    if index != utility.get_default_error() :
        print "found"
        md = mlist[index]
    else:
        print "not found"
    return md

def get_master_data_from_name(name, mlist):
    this_iso3 = ISO_countries.ISO3_from_name(name, csl)
    stats = get_master_data_from_iso3(this_iso3, mlist)
    return stats

def countries_with_no_master_data(mdlist, regs):
    tab5 = utility.grab_values_for_tag(mdlist, "Country_Name")
    tab1 = utility.grab_values_for_tag(regs, "Country_Name")
    diff = utility.set_difference(tab1, tab5)
    return diff
    
        
def to_json(filename, data):
	utility.to_json(filename, data)
	return

def to_csv(filename, data):
	utility.to_csv_from_OD(filename, data)
	return

if __name__ == '__main__':
    mdlist = build()

    #print mdlist

    to_xml(xml_target, mdlist)
    to_json(json_target, mdlist)
    to_csv(csv_target, mdlist)

    #print get_master_data_from_name("Jamaica", mdlist)

    tab5 = utility.grab_values_for_tag(mdlist, "Country_Name")
    tab1 = utility.grab_values_for_tag(regs, "Country_Name")
    diff = utility.set_difference(tab1, tab5)

    print "\n\nCountries with no master data: ", diff

