#! /usr/bin/env python

import csv
from political import Race
import os


def convert_state_races(csv_in):
    races = {}

    print("Building Races")
    # Determine Which Races Occured in election and the candidates
    with open(csv_in, 'r') as races_file:
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
    with open(csv_in, 'r') as results_file:
        results_read = csv.DictReader(results_file, delimiter=',')

    #     # Main File Processing
        for row in results_read:
            this_race = races[row['Race'] + ' ' + row['CountyCode']]
            race_rows = this_race.rows_to_write
            precinct = row['PrecinctName']

            try:
                if race_rows[precinct]:
                    race_rows[precinct][row['Candidate']] = row['Votes']
            except KeyError:
                race_rows[precinct] = {
                    row['Candidate']: row['Votes'],
                    'Row Label': row['PrecinctName'],
                    'County': row['CountyCode'],
                }

    # Export CSV FIles
    print("exporting results")
    subdir = os.path.join('Races', str(csv_in[0:8]))
    out_directory = os.path.join(os.getcwd(), subdir)

    if not os.path.exists(out_directory):
        print("made directory")
        os.makedirs(out_directory)
    else:
        print("Directory Exists")

    count = 0
    succesful_races = []

    for race, details in races.iteritems():

        for char in [".", " ", ",", "/"]:
            race = race.replace(char, "")

        file_out = os.path.join(out_directory, race + ".csv")

        with open(file_out, 'wr') as outfile:
            fields = ['Row Label', 'County']
            fields = fields + details.candidates
            writer = csv.DictWriter(outfile, fieldnames=fields)
            writer.writeheader()

            try:
                for k, v in details.rows_to_write.iteritems():
                    writer.writerow(v)
                succesful_races.append(race)
            except ValueError:
                count += 1

    # Stats readouts
    for race in succesful_races:
        print(race)

    print("Success rate {} of {}".format((len(races) - count), len(races)))

if __name__ == '__main__':
    convert_state_races('20141104_AllStatePrecincts.csv')
