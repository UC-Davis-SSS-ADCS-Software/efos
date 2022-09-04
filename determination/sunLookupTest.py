# imports
from sunLookup import sunLookup
import numpy as np
import csv
from datetime import datetime

# reads test input file and outputs results
def sunLookupTest(filename):
    outfile = open('sun_out.txt', 'w')
    with open(filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            print(row)
            startOfYear = row[0].find("2")
            date = datetime(int(str(row[0])[startOfYear:len(row[0])]), int(row[1]), int(row[2]))
            outputs = sunLookup(date)
            outstr = []
            for item in outputs:
                outstr.append(str(item))
            line = "\t".join(outstr) + "\n"
            outfile.write(line)
    outfile.close()
    print('Done')

sunLookupTest('sunLookupTestInputs.txt')