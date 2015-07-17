# /usr/bin/env

import csv
from political import Race
import os

RESULTS_CSV = '20141104_AllStatePrecincts.csv'
# RESULTS_CSV = '20140805_AllStatePrecincts.csv'
# RESULTS_CSV = 'test.csv'

# RACE_CSV = '20141104_AllState.csv'

races = {}

print("Building Races")
# Determine Which Races Occured in election and the candidates
with open(RESULTS_CSV, 'r') as races_file:
    race_read = csv.DictReader(races_file, delimiter=',')

    for row in race_read:
        current_row = Race(row['Race'], row['CountyCode'])
        current_race = str(current_row)

        if not(current_race in races):
            races[current_race] = current_row
            races[current_race].candidates = [row['Candidate']]
        else:
            if row['Candidate'] not in races[current_race].candidates:
                races[current_race].candidates.append(row['Candidate'])


# Open Results CSV file
print("Constructing rows")
with open(RESULTS_CSV, 'r') as results_file:
    results_read = csv.DictReader(results_file, delimiter=',')

    current_precinct = ''
    export_row = {}

    last_fn = set()

#     # Main File Processing
    for row in results_read:
        this_race = races[row['Race'] + ' ' + row['CountyCode']]

        if row['PrecinctName'] == current_precinct:
            export_row[row['Candidate']] = row['Votes']
        else:
            export_row = {
                row['Candidate']: row['Votes'],
                'Row Label': row['PrecinctName'],
                'PrecinctCode': row['PrecinctCode'],
                'County': row['CountyCode'],
                'Registered Voters': 'NULL'
            }
            current_precinct = row['PrecinctName']
#         # Compare the candidates in the row to export vs
#         # the total candidates to make sure the line is completed
#         # only when all candidates have been added to the export row
        final_names = set(this_race.candidates)
        current_names = set(export_row.keys())

        if not(final_names - current_names):
            this_race.rows_to_write.append(export_row)

            last_fn = set(export_row.keys())

out_directory = os.path.join(os.getcwd(), 'Races')

if not os.path.exists(out_directory):
    os.makedirs(out_directory)

# Write Rows to Files
for race, details in races.iteritems():

    for char in [".", " ", ",", "/"]:
        race = race.replace(char, "")

    file_out = os.path.join(out_directory, race + ".csv")

    with open(file_out, 'wr') as outfile:
        fields = ['Row Label', 'PrecinctCode', 'County', 'Registered Voters']
        fields = fields + details.candidates
        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()
        try:
            writer.writerows(details.rows_to_write)
        except ValueError as er:
            print race

"""
for file in directory

"""