import json
from pprint import pprint

source_json = "../output/countries_profile.json"

with open(source_json) as data_file:    
    data = json.load(data_file)

for n in range(0, len(data)):
	pprint(data[n]['country'])

print len(data)

