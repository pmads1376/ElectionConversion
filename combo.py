#! /usr/bin/env python

import os
import csv
from political import ComboRace


racedirectoy = '20141104'
subdirectory = os.path.join('Races', racedirectoy)
directory = os.path.abspath(os.path.join(os.getcwd(), subdirectory))

# out_directory = os.path.join(directory, "Joined_Races")
# if not(os.path.isdir(out_directory)):
#     print("Making Directory for Joined Races...")
#     os.mkdir(out_directory)
races = []
cmb_races = {}

for file_name in os.listdir(directory):
    if not os.path.isdir(file_name):
        print(file_name)
        # races.append(ComboRace(file_name, directory))
    else:
        print True

for cr in races:
    for other_cr in races:
        if cr is not other_cr:
            if cr == other_cr:
                if cr not in cmb_races.keys():
                    cmb_races[cr.race_name] = {}
                    cmb_races[cr.race_name][cr.county] = cr.rows
                    cmb_races[cr.race_name]['Candidates'] = cr.candidates
                print("test")
                cmb_races[cr.race_name][other_cr.county] = other_cr.rows

out_directory = os.path.join(directory, "Joined_Races")

if not(os.path.isdir(out_directory)):
    print("Making Directory for Joined Races...")
    os.mkdir(out_directory)


for name, values in cmb_races.iteritems():

    file_out = os.path.join(out_directory, name + ".csv")

    if 'KI' in values.keys():
        # print(name)
        pass
    else:
        with open(file_out, 'wr') as outfile:
            fields = ['Row Label', 'County'] + [x for x in values['Candidates']]
            writer = csv.DictWriter(outfile, fieldnames=fields)
            # print(type(name))
            writer.writeheader()

    # with open(os.path.join(cr.directory, cr.f), 'r') as sub_race:
    #     reader = csv.DictReader(sub_race, delimiter=',')


# count = 0
# for r in races:
#     # print r
#     # print r.candidates
#     if r.candidates == ['Yes', 'No']:
#         print r
#         count += 1
#     if r.candidates == ['Approved', 'Rejected']:
#         print r
#         count += 1
#     if r.candidates == ['Maintained', 'Repealed']:
#         print r
#         count += 1

# print count
