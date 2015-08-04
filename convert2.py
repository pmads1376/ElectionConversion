import csv
from political import Race, JoinedRace
import os

# 2014 Primary FIles
state_csv_in = '20140805_AllStatePrecincts.csv'
king_csv_in = '20140805_king.csv'

# 2014 General Files
state_csv_in = '20141104_AllStatePrecincts.csv'
king_csv_in = '20141104_king.csv'

# 2013 General Files
state_csv_in = '20131105_AllStatePrecincts_20131210_0314.csv'
king_csv_in = '20131105_king.csv'

# 2013 Primary FIles
state_csv_in = '20130806_AllStatePrecincts_20130823_1120.csv'
king_csv_in = '20130806_king.csv'


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

    # Open Stte CSV file
    print("Constructing rows for Non-King State Races")
    with open(state_csv_in, 'r') as results_file:
        results_read = csv.DictReader(results_file, delimiter=',')
        #  Get rows for various races
        for row in results_read:
            this_race = state_randc[row['Race'] + ' ' + row['CountyCode']]
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

    return state_randc


def convert_king_races(csv_in):
    races = {}
    king_only_candidates = [
        'Registered Voters',
        'Times Blank Voted',
        'Times Counted',
        'Times Over Voted',
        'Write-in'
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

            if row['CounterType'] not in king_only_candidates:
                try:
                    if rtw[precinct]:
                        rtw[precinct][row['CounterType']] = row['SumOfCount']
                except KeyError:
                    rtw[precinct] = {
                        row['CounterType']: row['SumOfCount'],
                        'Row Label': row['Precinct'],
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
            # print(r)

    shared_races = []
    un_state_races = []
    un_king_races = []

    for jr in k_races:
        for king in king_races.values():
            if 'KI' in jr.counties:
                if set(jr.candidates) == set(king.candidates):
                    if jr not in shared_races:
                        shared_races.append(jr)
                    elif 'Yes' in king.candidates:
                        if jr not in un_state_races:
                            un_state_races.append(jr)
                        if king not in un_king_races:
                            un_king_races.append(king)
                    elif 'Approved' in king.candidates:
                        if jr not in un_state_races:
                            un_state_races.append(jr)
                        if king not in un_king_races:
                            un_king_races.append(king)
                    elif 'Maintained' in king.candidates:
                        if jr not in un_state_races:
                            un_state_races.append(jr)
                        if king not in un_king_races:
                            un_king_races.append(king)
                    else:
                        print("candidates faile: {}".format(jr))
                        if jr not in un_state_races:
                            un_state_races.append(jr)
                        if king not in un_king_races:
                            un_king_races.append(king)

                    if jr in shared_races:
                        jr.rows.append([row for row in king.rows_to_write.values()])

    for r in k_races:
        if r not in shared_races:
            un_state_races.append(r)

    print("Number of state races listing KI is: {}".format(len(k_races)))
    # print("There are {} races that don't have unique candidates".format(len(unique_races)))
    print("There are {} unique state races and {} unique king races".format(len(un_state_races), len(un_king_races)))
    print("The number of matches is: {}".format(len(shared_races)))

    manual_joins = {}

    for r_ in un_state_races:
        manual_joins[r_.race_name] = r_
        del(joined_races[r_.race_name])

    for r_ in un_king_races:
        if r_.race_name not in manual_joins:
            manual_joins[r_.race_name] = r_
        else:
            print("It actually matched?")

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

    count_export = 0
    unsuccesful_races = []

    for jr in joined_races.values():

        race = jr.race_name

        for char in [".", " ", ",", "/"]:
            race = race.replace(char, "")

        file_out = os.path.join(out_directory, race + ".csv")

        with open(file_out, 'wr') as outfile:
            rowkeys = ['Row Label', 'County']
            rowkeys += jr.candidates

            writer = csv.DictWriter(outfile, fieldnames=rowkeys)
            writer.writeheader()

            try:
                if type(jr) == Race:
                    writer.writerows(jr.rows_to_write.values())
                else:
                    for row in jr.rows:
                        writer.writerows(row)
            except ValueError as e:
                print(e)
                print(jr.rows[0])
                count_export += 1

    print("Success rate {} of {}".format((len(joined_races) - count_export), len(joined_races)))

    for r in unsuccesful_races:
        print(r)

if __name__ == '__main__':
    state_race = convert_state_races(state_csv_in)
    king_race = convert_king_races(king_csv_in)
    joined_races, manual_joins = combine_races(state_race, king_race)
    export_joined_files(joined_races, str(state_csv_in[0:8]))
    export_joined_files(manual_joins, 'Manual' + str(state_csv_in[0:8]))
