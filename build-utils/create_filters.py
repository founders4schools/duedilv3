#
import csv

print
print '####### Company search filters'
print

with open('search-companies.csv', 'rb') as csv_in_file:
    reader = csv.DictReader(csv_in_file)
    f_list = []
    for row in reader:
        var = row['Filter Name']
        print '{0!s} = "{1!s}" # {2!s}'.format(var.upper(), var, row['Type'])
        print '#', row['Description']
        print
        f_list.append(var.upper())
    print 'COMPANY_FILTERS = ['
    for v in f_list:
        print '{0!s},'.format(v)
    print ']'

print
print '### company Range filters'
print

with open('filter-companies.csv', 'rb') as csv_in_file:
    reader = csv.DictReader(csv_in_file)
    f_list = []
    for row in reader:
        var = row['Field Name']
        print '{0!s} = "{1!s}" # {2!s}'.format(var.upper(), var, row['Optional'])
        print '#', row['Description']
        f_list.append(var.upper())
        print
    print 'COMPANY_RANGE_FILTERS = ['
    for v in f_list:
        print '{0!s},'.format(v)
    print ']'

print
print '####director search '
print

with open('search-directors.csv', 'rb') as csv_in_file:
    reader = csv.DictReader(csv_in_file)
    f_list = []
    for row in reader:
        var = row['Field Name']
        print '{0!s} = "{1!s}" # {2!s}'.format(var.upper(), var, row['Type'])
        print '#', row['Description']
        print
        f_list.append(var.upper())
    print 'DIRECTOR_FILTERS = ['
    for v in f_list:
        print '{0!s},'.format(v)
    print ']'

print
print '######### director range filters '
print

with open('filter-directors.csv', 'rb') as csv_in_file:
    reader = csv.DictReader(csv_in_file)
    f_list = []
    for row in reader:
        var = row['Field Name']
        print '{0!s} = "{1!s}" # {2!s}'.format(var.upper(), var, row['Type'])
        print '#', row['Description']
        print
        f_list.append(var.upper())
    print 'DIRECTOR_RANGE_FILTERS = ['
    for v in f_list:
        print '{0!s},'.format(v)
    print ']'
