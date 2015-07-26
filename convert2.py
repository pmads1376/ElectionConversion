import csv
from political import Race, JoinedRace
import os

state_csv_in = '20141104_AllStatePrecincts.csv'
king_csv_in = '20141104ecanvass.csv'


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

    print("Building King race and candidates")
    # Determine Which Races Occured in election and the candidates
    with open(csv_in, 'r') as races_file:
        race_read = csv.DictReader(races_file, delimiter=',')
        king_only_candidates = [
            'Registered Voters',
            'Times Blank Voted',
            'Times Counted',
            'Times Over Voted',
            'Write-in'
        ]

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

            # print(row['CounterType'])
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
            joined_races[name] = JoinedRace(name, race.candidates, rtw)
            joined_races[name].counties = [race.county]
        elif(race.candidates == joined_races[name].candidates):
            joined_races[name].rows.append(rtw)
            joined_races[name].counties.append(race.county)

    count = 0
    for jr in joined_races.values():
        for race in king_races.values():
            if jr.candidates == race.candidates:
                # print(jr.race_name)
                if 'KI' in jr.counties:
                    print(jr.candidates)
                    print(race.candidates)
                    print(jr.counties)
                    if jr.candidates == ['Yes', 'No']:
                        # print(jr.race_name)
                        # print(race)
                        count += 1
                    elif jr.candidates == ['Approved', 'Rejected']:
                        # print(jr.race_name)
                        # print(race)
                        count += 1
                    elif jr.candidates == ['Repealed', 'Maintained']:
                        # print(race)
                        # print(jr.race_name)
                        count += 1

    print(count)

    return joined_races


# Export CSV FIles
def export_files(joined_races):
    print("exporting results")
    subdir = os.path.join('Races', str(state_csv_in[0:8]))
    out_directory = os.path.join(os.getcwd(), subdir)

    if not os.path.exists(out_directory):
        print("made directory")
        os.makedirs(out_directory)
    else:
            print("Directory Exists")

    # count = 0
    # succesful_races = []

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
                for row in jr.rows:
                    writer.writerows(row)
            except ValueError:
                for row in jr.rows:
                    print(row)


# print("Success rate {} of {}".format((len(joined_races) - count), len(joined_races)))
if __name__ == '__main__':
    state_race = convert_state_races(state_csv_in)
    king_race = convert_king_races(king_csv_in)
    joined_races = combine_races(state_race, king_race)
