import utility 
from collections import OrderedDict

filename = "../source_data/Special_Characters.xlsx"
mappings = ["Name", "Character", "Unicode_CodePoint", "Substitute","Standard",	"Description"] 

global charset 
charset = []

def build():
	charset = utility.from_excelsheet(filename, 0, 1, mappings)
	return charset

def xml_safe(stri, charset):
    if len(charset) == 0:
        charset = utility.from_excelsheet(filename, 0, 1, mappings)     
    retstr = stri
    for x in range(0, len(charset)): 
        curchar = charset[x]
        curkey = curchar['Character']
        curvalue = curchar['Substitute']
        retstr = retstr.replace(curkey, curvalue)
    return retstr

    

if __name__ == '__main__':
    charset = build()
    print xml_safe("Asia & Africa", charset)
    print xml_Safe(c, charset)
