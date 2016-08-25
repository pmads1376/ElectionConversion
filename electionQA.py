#collect all legislatie representative 
#tally total votes for each candidate

import os
import csv
import re

def createLegSummary():
    print("Starting Summary")
    rootdir = os.path.join(os.getcwd(), "Races")
    out_file = os.path.join(rootdir, 'legislativeSummary.csv')
    districts = {}

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if 'Legislative' in file and 'Representative' in file:
                numArray = re.findall(r'[0-9]+', file)
                districtNum = numArray[0]
                                
                candidateTotalCounts = {}
                
                with open(os.path.join(subdir, file), 'r') as cur_file:
                    current = csv.DictReader(cur_file, delimiter=',')
                    
                    count = 0
                    for row in current:
                        for votes in row.values():
                            try:
                                count += int(votes)
                            except ValueError:
                                count += 0
                                
                    keyName = "Position 1" if numArray[1] == "1" else "Position 2"
                    
                    try:
                        districts[districtNum][keyName] = str(count)
                    except KeyError:
                        districts[districtNum] = {}
                        districts[districtNum][keyName] = str(count)
    
    print(districts)
    with open(out_file, 'w', newline="\n", encoding="utf-8") as outfile:
        rowkeys = ["District", "Position 1", "Position 2"]
        writer = csv.DictWriter(outfile, fieldnames=rowkeys)
        writer.writeheader()
        
        for k, v in districts.items():
            row = {}
            row["District"] = k
            row["Position 1"] = v["Position 1"]
            row["Position 2"] = v["Position 2"]
            writer.writerow(row)
                    
def runQA():
    createLegSummary()

if __name__ == '__main__':
    print("Running QA script")
    runQA()
    print("QA Completed")