import csv

with open('company-key-info-response.csv', 'rb') as csv_in_file:
    reader = csv.DictReader(csv_in_file)
    f_list = []
    for row in reader:
        var = row['Field Name']
        print "'{0!s}',".format(var)
        print '#', row['Type'], row['Description']

print
print '#########################'
print

with open('company-registered-address.csv', 'rb') as csv_in_file:
    reader = csv.DictReader(csv_in_file)
    f_list = []
    for row in reader:
        var = row['Field Name']
        print "'{0!s}',".format(var)
        print '#', row['Type'], row['Description']
