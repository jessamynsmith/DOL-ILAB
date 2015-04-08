
import xlrd
import pyodbc
import json
import collections

 
filename = 'goods_2010_2014.xls' 
name_no_ext = filename.split('.')[0]
print name_no_ext

# Open the workbook and select the first worksheet
wb = xlrd.open_workbook(filename)
sh = wb.sheet_by_index(0)
 
# List to hold dictionaries
goods_list = []

countries = []

goods = []
 
# Iterate through each row in worksheet and fetch values into dict
for rownum in range(1, sh.nrows):
    good = OrderedDict()
    row_values = sh.row_values(rownum)
    good['Year'] = int(row_values[0])
    good['Country'] = row_values[1]
    if row_values[1] not in countries:
    	countries.append(str(row_values[1]))
    good['Good'] = row_values[2]
    if row_values[2] not in goods:
    	goods.append(str(row_values[2]))
    good['Child Labor'] = row_values[3]
    good['Forced Labor'] = row_values[4]
    goods_list.append(good)
 
print countries

print "\n" 

print goods 


 
connstr = 'DRIVER={mySQL};SERVER=localhost;DATABASE=DOLILAB;'
conn = pyodbc.connect(connstr)
cursor = conn.cursor()
 
cursor.execute("""
            SELECT ID, FirstName, LastName, Street, City, ST, Zip
            FROM Students
            """)
 
rows = cursor.fetchall()
 
# Convert query to row arrays
 
rowarray_list = []
for row in rows:
    t = (row.ID, row.FirstName, row.LastName, row.Street, 
         row.City, row.ST, row.Zip)
    rowarray_list.append(t)
 
j = json.dumps(rowarray_list)
rowarrays_file = 'student_rowarrays.js'
f = open(rowarrays_file,'w')
print >> f, j
 
# Convert query to objects of key-value pairs
 
objects_list = []
for row in rows:
    d = collections.OrderedDict()
    d['id'] = row.ID
    d['FirstName'] = row.FirstName
    d['LastName'] = row.LastName
    d['Street'] = row.Street
    d['City'] = row.City
    d['ST'] = row.ST
    d['Zip'] = row.Zip
    objects_list.append(d)
 
j = json.dumps(objects_list)
objects_file = 'student_objects.js'
f = open(objects_file,'w')
print >> f, j
 
conn.close()
