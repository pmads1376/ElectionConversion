#! /usr/bin/env python

import os
from political import Race as r
# import re

# join logic for subdirectory races
racedirectoy = '20141104'
subdirectory = os.path.join('Races', racedirectoy)
directory = os.path.abspath(os.path.join(os.getcwd(), subdirectory))
out_directory = os.path.join(directory, "Joined_Races")

if not(os.path.isdir(out_directory)):
    print("Making Directory for Joined Races...")
    os.mkdir(out_directory)

multi_county_races = []
combined_races = {}
# king_races = {}

for file_name in os.listdir(directory):
    if not("COUNTYWIDE" in file_name):
        multi_county_races.append(file_name[:-4])

for f in multi_county_races:
    for other_f in multi_county_races:

    # for other_files in multi_county_races:
    #     if other_files is not f:
    #         try:
    #             if other_files[:-2] == f[:-2]:
    #                 combined_races[f[:-2]].append(other_files)
    #         except KeyError:
    #             combined_races[f[:-2]] = [f, other_files]

# # print(combined_races.popitem())

for k, v in combined_races.iteritems():
    if 'LegislativeDistrict' not in k:
        print("{} has {} counties".format(k, len(v)))

    # file_out = os.path.join(out_directory, k + ".csv")

    # # standarize columns
    # with open(file_out, 'wr') as outfile:
    #     pass

# if candidates match join files