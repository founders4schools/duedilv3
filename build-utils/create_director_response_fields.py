from __future__ import print_function
import csv

with open('director-key-info-response.csv', 'rb') as csv_in_file:
    reader = csv.DictReader(csv_in_file)
    f_list = []
    print ('# key info')
    for row in reader:
        var = row['Field Name']
        print ("'{0!s}',".format(var))
        print ('#', row['Type'], row['Description'])

print()
print ('#########################')
print()

with open('director-directorships.csv', 'rb') as csv_in_file:
    reader = csv.DictReader(csv_in_file)
    f_list = []
    print ('# directorships')
    for row in reader:
        var = row['Field Name']
        print ("'{0!s}',".format(var))
        print ('#', row['Type'], row['Description'])

print()
print ('#########################')
print()
