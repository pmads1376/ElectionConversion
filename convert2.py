import csv
from political import Race, JoinedRace
import os

race_candidate = {}

state_csv_in = '20141104_AllStatePrecincts.csv'

print("Building Non-King State race_candidate")
# Determine Which race_candidate Occured in election and the candidates
with open(state_csv_in, 'r') as races_file:
    race_read = csv.DictReader(races_file, delimiter=',')

    for row in race_read:
        cur_row = Race(row['Race'], row['CountyCode'])
        cur_race = str(cur_row)

        if not(cur_race in race_candidate):
            race_candidate[cur_race] = cur_row
            race_candidate[cur_race].candidates = [row['Candidate']]
        else:
            if row['Candidate'] not in race_candidate[cur_race].candidates:
                race_candidate[cur_race].candidates.append(row['Candidate'])


# Open Results CSV file
print("Constructing rows for Non-King State Races")
with open(state_csv_in, 'r') as results_file:
    results_read = csv.DictReader(results_file, delimiter=',')
    #  Get rows for various races
    for row in results_read:
        this_race = race_candidate[row['Race'] + ' ' + row['CountyCode']]
        rtw = this_race.rows_to_write
        precinct = row['PrecinctName']

        try:
            if rtw[precinct]:
                rtw[precinct][row['Candidate']] = row['Votes']
        except KeyError:
            rtw[precinct] = {
                row['Candidate']: row['Votes'],
                'Row Label': row['PrecinctName'],
                'County': row['CountyCode'],
            }

print("Combine Races")

joined_races = {}

for race in race_candidate.values():
    name = race.race_name
    rtw = race.rows_to_write.values()

    if name not in joined_races.keys():
        joined_races[name] = JoinedRace(name, race.candidates, rtw)
        joined_races[name].counties = [race.county]
    elif(race.candidates == joined_races[name].candidates):
        joined_races[name].rows.append(rtw)
        joined_races[name].counties.append(race.county)

# count = 0
# for r in joined_races.values():
#     print(r)
#     count+=1

# print(count)
    # Export CSV FIles
print("exporting results")
subdir = os.path.join('Races', str(state_csv_in[0:8]))
out_directory = os.path.join(os.getcwd(), subdir)

if not os.path.exists(out_directory):
    print("made directory")
    os.makedirs(out_directory)
else:
        print("Directory Exists")

count = 0
succesful_races = []

for jr in joined_races.values():

    for char in [".", " ", ",", "/"]:
        race = jr.race_name.replace(char, "")

    file_out = os.path.join(out_directory, race + ".csv")

    with open(file_out, 'wr') as outfile:
        fields = ['Row Label', 'County']
        fields = fields + jr.candidates
        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()

        rowkeys = []

        for row in jr.rows:
            try:
                    # for row in jr.rows:
                    writer.writerow(row)
                    # print(row)
            except ValueError as e:
                # succesful_races.append(race)
                # for d in row:
                #     for key in d.keys():
                #         if key not in rowkeys:
                #             rowkeys.append(key)
                # print(jr.race_name)
                # print(fields)
                # print(rowkeys)
                # print(type(row))
                # print('*****************')
                print e
                count += 1

    # Stats readouts
for race in succesful_races:
    print(race)

print("Success rate {} of {}".format((len(joined_races) - count), len(joined_races)))

# if __name__ == '__main__':
#     convert_state_races('20141104_AllStatePrecincts.csv')
