import goods
import sectors
from collections import OrderedDict

secs = sectors.build()

def build():

	results = []

	for sector in secs:
		newr = OrderedDict()
		newr['Good_Name'] = sector['Good_Name']
		newr['Good_Sector'] = sector['Good_Sector']


	return results



if __name__ == '__main__':
	
	goods = build()

