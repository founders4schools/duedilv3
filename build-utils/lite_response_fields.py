from __future__ import print_function

import csv

with open('lite-response.csv', 'rb') as csv_in_file:
    reader = csv.DictReader(csv_in_file)
    f_list = []
    print ('# search response')
    for row in reader:
        var = row['Field Name']
        print ("'%s'," % var)
        print ('#', row['Type'], row['Description'])

print()
print ('#########################')
print()

with open('lite-company.csv', 'rb') as csv_in_file:
    reader = csv.DictReader(csv_in_file)
    f_list = []
    print ('# company')
    for row in reader:
        var = row['Field Name']
        print ("'%s'," % var)
        print ('#', row['Type'], row['Description'])

print()
print ('#########################')
print()
