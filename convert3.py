import csv
from political import Race, JoinedRace
import os
import electionQA

files = []

# 2014 Primary FIles
state_csv_in = '20160802_AllStatePrecinctsPrimary.csv'
king_csv_in = '20160802_KingPrimary.csv'
files.append((state_csv_in, king_csv_in))


def convert_state_races(csv_in):
    state_randc = {}

    print("Building Non-King State state_randc")
    # Determine Which state_randc Occured in election and the candidates
    with open(csv_in, 'r') as races_file:
        race_read = csv.DictReader(races_file, delimiter=',')

        for row in race_read:
            cur_row = Race(row['Race'], row['CountyCode'])
            cur_race = str(cur_row)

            if not(cur_race in state_randc):
                state_randc[cur_race] = cur_row
                state_randc[cur_race].candidates = [row['Candidate']]
            else:
                if row['Candidate'] not in state_randc[cur_race].candidates:
                    state_randc[cur_race].candidates.append(row['Candidate'])

            #if "Registered Voters" not in state_randc[cur_race].candidates:
            #    state_randc[cur_race].candidates.append("Registered Voters")

    # Open Stte CSV file
    print("Constructing rows for Non-King State Races")
    with open(state_csv_in, 'r') as results_file:
        results_read = csv.DictReader(results_file, delimiter=',')
        #  Get rows for various races
        for row in results_read:
            this_race = state_randc[row['Race'] + ' ' + row['CountyCode']]
            rtw = this_race.rows_to_write
            precinct = row['PrecinctName']
            if ";" in precinct:
                    precinct = precinct.replace(";", "")

            try:
                if rtw[precinct]:
                    rtw[precinct][row['Candidate']] = row['Votes']
            except KeyError:
                rtw[precinct] = {
                    row['Candidate']: row['Votes'],
                    'Row Label': precinct,
                    'County': row['CountyCode']
                }

    return state_randc


def convert_king_races(csv_in):
    races = {}
    king_only_candidates = [
        'Registered Voters',
        'Times Blank Voted',
        'Times Counted',
        'Times Over Voted',
        'Write-In'
    ]

    print("Building King race and candidates")
    # Determine Which Races Occured in election and the candidates
    with open(csv_in, 'r') as races_file:
        race_read = csv.DictReader(races_file, delimiter=',')

        for row in race_read:
            current_row = Race(row['Race'], 'KI')
            current_race = str(current_row)

            if row['CounterType'] not in king_only_candidates:
                if not(current_race in races):
                    races[current_race] = current_row
                    races[current_race].candidates = [row['CounterType']]
                else:
                    if row['CounterType'] not in races[current_race].candidates:
                        races[current_race].candidates.append(row['CounterType'])

    # Open Results CSV file
    print("Constructing rows for King Races")
    with open(csv_in, 'r') as results_file:
        results_read = csv.DictReader(results_file, delimiter=',')

    #     # Main File Processing
        for row in results_read:
            this_race = races[row['Race'] + ' ' + 'KI']
            rtw = this_race.rows_to_write
            precinct = row['Precinct']
            
            if ";" in precinct:
                    precinct = precinct.replace(";", "")

            if row['CounterType'] not in king_only_candidates:
                try:
                    if rtw[precinct]:
                        rtw[precinct][row['CounterType']] = row['SumOfCount']
                except KeyError:
                    rtw[precinct] = {
                        row['CounterType']: row['SumOfCount'],
                        'Row Label': precinct,
                        'County': 'KI',
                    }

    return races


def combine_races(state_races, king_races):
    print("Combine Races")

    joined_races = {}

    for race in state_races.values():
        name = race.race_name
        rtw = race.rows_to_write.values()

        if name not in joined_races.keys():
            joined_races[name] = JoinedRace(name, race.candidates, race.county, rtw)
            joined_races[name].counties = [race.county]
        elif(race.candidates == joined_races[name].candidates):
            joined_races[name].rows.append(rtw)
            joined_races[name].counties.append(race.county)

    k_races = []

    for r in joined_races.values():
        if 'KI' in r.counties:
            k_races.append(r)

    review_races = []

    for race in k_races:
        for other_race in king_races.values():
            if set(race.candidates) == set(other_race.candidates):
                print("match")
                if 'Yes' in other_race.candidates:
                    if race not in review_races:
                        review_races.append(race)
                    if other_race not in review_races:
                        review_races.append(other_race)
                elif 'Approved' in other_race.candidates:
                    if race not in review_races:
                        review_races.append(race)
                    if other_race not in review_races:
                        review_races.append(other_race)
                elif 'Maintained' in other_race.candidates:
                    if race not in review_races:
                        review_races.append(race)
                    if other_race not in review_races:
                        review_races.append(other_race)
                else:
                    race.rows.append([row for row in other_race.rows_to_write.values()])

    manual_joins = {}

    for race in review_races:
        manual_joins[race.race_name] = race

    print("{} list and {} dict".format(len(review_races), len(manual_joins.keys())))

    return (joined_races, manual_joins)


# Export CSV FIles
def export_joined_files(joined_races, subdir_name):
    print("exporting results for {}".format(subdir_name))
    subdir = os.path.join('Races', subdir_name)
    out_directory = os.path.join(os.getcwd(), subdir)

    if not os.path.exists(out_directory):
        print("made directory")
        os.makedirs(out_directory)
    else:
            print("Directory Exists")
            # pass

    count_export = 0
    unsuccesful_races = []

    # print("length of joined races {}:".format(len(joined_races.values())))

    for jr in joined_races.values():
        race = jr.race_name

        for char in [".", " ", ",", "/"]:
            race = race.replace(char, "")

        file_out = os.path.join(out_directory, race + ".csv")

        with open(file_out, 'a', newline="\n", encoding="utf-8") as outfile:
            rowkeys = ['Row Label', 'County']
            rowkeys += jr.candidates
            #if "Registered Voters" not in jr.candidates:
            #    rowkeys.append("Registered Voters")

            writer = csv.DictWriter(outfile, fieldnames=rowkeys)
            writer.writeheader()

            try:
                if type(jr) == Race:
                    for r in jr.rows_to_write.values():
                        if 'Total' not in r['Row Label']:
                            writer.writerow(r)
                else:
                    for row in jr.rows:
                        for r in row:
                            if 'Total' not in r['Row Label']:
                                writer.writerow(r)
            except ValueError as e:
                print(e)
                print(jr.rows[0][0])
                count_export += 1

    # print("Success rate {} of {}".format((len(joined_races) - count_export), len(joined_races)))

    for r in unsuccesful_races:
        print(r)   

if __name__ == '__main__':
    for state_csv_in, king_csv_in in files:
        state_race = convert_state_races(state_csv_in)
        king_race = convert_king_races(king_csv_in)
        joined_races, manual_joins = combine_races(state_race, king_race)
        export_joined_files(joined_races, str(state_csv_in[0:8]))
        export_joined_files(manual_joins, 'Manual' + str(state_csv_in[0:8]))
        electionQA.runQA()