import csv
from political import Race

RESULTS_CSV = '20141104_AllStatePrecincts.csv'
# RESULTS_CSV = 'test.csv'

# RACE_CSV = '20141104_AllState.csv'

races = {}

print("Building Races")
# Determine Which Races Occured in election and the candidates
with open(RESULTS_CSV, 'r') as races_file:
    race_read = csv.DictReader(races_file)

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
    results_read = csv.DictReader(results_file)

    current_precinct = ''
    export_row = {}

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
            this_race.rows_to_write[current_precinct] = export_row

# Write Rows to Files
for race, details in races.iteritems():
    file_name = race.replace(".", "") + ".csv"
    file_name = file_name.replace(" ", "")

    print(race)
    for row in details.rows_to_write.values():
        print(row)

    # with open(file_name, 'w') as outfile:
    #     fields = ['Row Label', 'PrecinctCode', 'County', 'Registered Voters']
    #     print(details.candidates)
    #     fields = fields + details.candidates

    #     writer = csv.DictWriter(outfile, fieldnames=fields)
    #     writer.writeheader()
        # for precinct in details.rows_to_write.values():
        #     writer.writerow(precinct)
