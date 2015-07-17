# /usr/bin/env

import csv
from political import Race
import os

# RESULTS_CSV = '20141104_AllStatePrecincts.csv'
# RESULTS_CSV = '20140805_AllStatePrecincts.csv'
# RESULTS_CSV = 'test.csv'
RESULTS_CSV = 'ecanvass.csv'

# RACE_CSV = '20141104_AllState.csv'

races = {}

print("Building Races")
# Determine Which Races Occured in election and the candidates
with open(RESULTS_CSV, 'r') as races_file:
    race_read = csv.DictReader(races_file, delimiter=',')

    for row in race_read:
        current_row = Race(row['Race'], 'KI')
        current_race = str(current_row)

        if not(current_race in races):
            races[current_race] = current_row
            races[current_race].candidates = [row['CounterType']]
        else:
            if row['CounterType'] not in races[current_race].candidates:
                races[current_race].candidates.append(row['CounterType'])


# Open Results CSV file
print("Constructing rows")
with open(RESULTS_CSV, 'r') as results_file:
    results_read = csv.DictReader(results_file, delimiter=',')

    current_precinct = ''
    export_row = {}

    last_fn = set()

#     # Main File Processing
    for row in results_read:
        this_race = races[row['Race'] + ' ' + 'KI']

        if row['Precinct'] == current_precinct:
            export_row[row['CounterType']] = row['SumOfCount']
        else:
            export_row = {
                row['CounterType']: row['SumOfCount'],
                'Row Label': row['Precinct'],
                'PrecinctCode': row['Precinct'],
                'County': 'KI',
                'Registered Voters': 'NULL'
            }
            current_precinct = row['Precinct']
#         # Compare the candidates in the row to export vs
#         # the total candidates to make sure the line is completed
#         # only when all candidates have been added to the export row
        final_names = set(this_race.candidates)
        current_names = set(export_row.keys())

        if not(final_names - current_names):
            this_race.rows_to_write.append(export_row)

            last_fn = set(export_row.keys())

# Export CSV FIles
print("exporting results")
out_directory = os.path.join(os.getcwd(), 'Races')

if not os.path.exists(os.path.join(out_directory, "King")):
    print("made directory")
    os.makedirs(os.path.join(out_directory, "King"))
else:
    print("Directory Exists")

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
            print(er)
            print(len(details.rows_to_write))

"""
for file in directory

"""