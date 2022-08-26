# Test of SGP4 Orbit Propagator
from sgp4.api import Satrec
import csv

outfile = open('sgp4_out.txt', 'w')
with open('testInputsSGP4.txt') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        tle1 = row[0]
        tle2 = row[1]
        tle1 = tle1.strip("'")
        tle2 = tle2.strip("'")
        try:
            jd = float(row[2])
            fr = float(row[3])
        except:
            continue
        satellite = Satrec.twoline2rv(tle1, tle2)
        e, r, v = satellite.sgp4(jd, fr)
        outstr = []
        for item in r:
            outstr.append(str(item))
        for item in v:
            outstr.append(str(item))
        line = "\t".join(row)+"\t"+"\t".join(outstr) + "\n"
        outfile.write(line)
outfile.close()
print('Done')