# imports
import pyIGRF
import numpy as np
import csv

# lat, longitude in degrees
# altitude in m
# decimal date (i.e. 2022.5)
# modified version of IGRF for testing
def igrf_lat_lon(lat, lon, alt, decimal_date):

    # get magnetic field in ecef frame
    r = pyIGRF.igrf_value(lat, lon, alt, decimal_date) # get magnetic field parameters
    vector = np.array([r[3], r[4], r[5]]) # save north, east, and vertical components of magnetic field in nT
    mag_vector_ecef = vector / np.linalg.norm(vector) # normalize
    return mag_vector_ecef

# reads test input file and outputs results
def igrf_test_inputs(filename):
    outfile = open('igrf_out.txt', 'w')
    print("Latitude, Longitude, Altitude, Decimal Date, Mag Vector")
    with open(filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            outputs = igrf_lat_lon(float(row[0]), float(row[1]), float(row[2]), float(row[3]))
            outstr = []
            for item in outputs:
                outstr.append(str(item))
            line = "\t".join(row)+"\t"+"\t".join(outstr) + "\n"
            outfile.write(line)
    outfile.close()
    print('Done')

igrf_test_inputs('inputs.txt')
