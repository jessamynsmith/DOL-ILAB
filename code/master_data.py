 

import utility
import regions
import special_chars
import ISO_countries
from collections import OrderedDict

csv_2013_target = '../output/2013/extra/master_data_from_XL.csv' 
xml_2013_target = '../output/2013/extra/master_data_from_XL.xml' 
json_2013_target = '../output/2013/extra/master_data_from_XL.json' 

csv_2014_target = '../output/2014/extra/master_data_from_XL.csv' 
xml_2014_target = '../output/2014/extra/master_data_from_XL.xml' 
json_2014_target = '../output/2014/extra/master_data_from_XL.json' 

cur_year = 2013

regs = regions.build(cur_year)
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

def get_cur_year():
    return cur_year

def set_cur_year(yr):
    cur_year = yr
    return

def set_regions(yr):
    regs = regions.build(yr)
    return

def build(year):
    master_data = utility.from_excelsheet(utility.get_source_filename(year), 4, 1, mappings)
    results = include_extra(master_data, year)
    return results

def include_extra(masterdata, year):
    md_list = []
    if year != get_cur_year():
        print "Switching years from ", get_cur_year(), " to ", year
        set_regions(year)
        set_cur_year(year)
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

def prettify(list2, separator):
    res_str = "\n"
    for item in list2:
        res_str = res_str + str(item) + separator
    return res_str

def get_country_name(iso3):
    result = regions.find_X_from_Y("Country_Name", "Country_ISO3", regs, iso3)
    return result

if __name__ == '__main__':
    mdlist_2013 = build(2013)
    mdlist_2014 = build(2014)

    to_xml(xml_2013_target, mdlist_2013)
    to_json(json_2013_target, mdlist_2013)
    to_csv(csv_2013_target, mdlist_2013)

    to_xml(xml_2014_target, mdlist_2014)
    to_json(json_2014_target, mdlist_2014)
    to_csv(csv_2014_target, mdlist_2014)

    set_regions(2013)
    tab4_2013 = utility.grab_values_for_tag(mdlist_2013, "Country_ISO3")
    tab1_2013 = utility.grab_values_for_tag(regs, "Country_ISO3")
    diff_2013 = utility.set_difference(tab1_2013, tab4_2013)
    print "\nCountries with no stats (for 2013): ", prettify(map(get_country_name, diff_2013), "\n")
    
    set_regions(2014)
    tab4_2014 = utility.grab_values_for_tag(mdlist_2014, "Country_ISO3")
    tab1_2014 = utility.grab_values_for_tag(regs, "Country_ISO3")
    diff_2014 = utility.set_difference(tab1_2014, tab4_2014)
    print "\nCountries with no stats (for 2014): ", prettify( map(get_country_name, diff_2014), "\n")

