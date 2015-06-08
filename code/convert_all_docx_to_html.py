from os import listdir
from os.path import isfile, join
import commands

sourcepath = "../source_data/countries/2013/docx/"
targetpath = "../source_data/countries/2013/html/"
fullstop = "."
html_ext =".html"
abiword_cmd = "/Applications/abiword -t "


def convert_doc_to_html(filename):
	sourcefp = sourcepath + filename

	k = filename.rfind(fullstop)
	out_file = targetpath+filename[:k]+html_ext

	convert_state = abiword_cmd + sourcefp + ' ' + out_file

	#print convert_state
	out = commands.getoutput(convert_state)

	return


def convert_all():

	filenames = [ filename for filename in listdir(sourcepath) if isfile(join(sourcepath,filename)) ]

	for filename in filenames:
		convert_doc_to_html(filename)
	
	return


if __name__ == '__main__':
	convert_all()	






