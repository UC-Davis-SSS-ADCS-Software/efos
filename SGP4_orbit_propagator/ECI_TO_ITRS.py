from astropy.coordinates.representation import BaseRepresentation, CartesianRepresentation
from astropy.coordinates.earth import BaseGeodeticRepresentation
from astropy.coordinates import ITRS, TEME
from astropy.units import Quantity
from astropy.time import Time


# SGP4 (TLE to X_ECI, V_ECI)

import numpy as np
from sgp4.api import Satrec, jday

# function to parse datetime string and extract year,month,day,hour,min,sec
def parse_time(datetime):
    year,month,day,hour,minute,sec = datetime.split(",",5)
    return np.array([year,month,day,hour,minute,sec])

# function using SGP4 to convert TLE to ECI frame vectors
# s, t are first and second lines of TLE respectively in string format
# Example below
# s = '1 25544U 98067A   21364.58225513  .00006501  00000-0  12261-3 0  9994'
# t = '2 25544  51.6441 91.5424 0004841  342.0852  149.8473 15.49806377319031'
# datetime should be a datetime string in format 'year,month,day,hour,min,sec'
def TLE_to_pos_vel(s, t, datetime):
    satellite = Satrec.twoline2rv(s, t)
    time_str = parse_time(datetime)
    jd, fr = jday(float(time_str[0]),float(time_str[1]),float(time_str[2]),float(time_str[3]),float(time_str[4]),float(time_str[5]))
    e, r, v = satellite.sgp4(jd, fr)
    # return array where first row is X_ECI, second row is V_ECI
    return np.array([
        [r[0], r[1], r[2]],
        [v[0], v[1], v[2]]
        ])


#largely from https://docs.astropy.org/en/stable/coordinates/satellites.html
#time_arr is the 2D output of TLE_to_pos_vel()
#datetime should be a datetime string in format 'year,month,day,hour,min,sec'
def ECI_TO_ITRS(teme_arr, datetime):
    time_str = parse_time(datetime)
    jd, fr = jday(float(time_str[0]),float(time_str[1]),float(time_str[2]),float(time_str[3]),float(time_str[4]),float(time_str[5]))
    teme = TEME(
        CartesianRepresentation(
            Quantity(teme_arr[0][0], 'km'),
            Quantity(teme_arr[0][1], 'km'),
            Quantity(teme_arr[0][2], 'km'),
            copy = True),
        obstime = Time(jd, fr, "jd"),
        copy = True
    )
    location = teme.transform_to(ITRS(obstime = Time(jd, fr, "jd"))).earth_location
    return [location.lat, location.lon, location.height]


#latest ISS TLE: 
# ISS (ZARYA)             
# 1 25544U 98067A   22308.86337963  .00016735  00000+0  30304-3 0  9994
# 2 25544  51.6449 359.6935 0006351  41.3591 303.6163 15.49753126366997
#compare to http://wsn.spaceflight.esa.int/iss/index_portal.php
def main():
    datetime = "2022,11,5,6,11,0"
    teme = TLE_to_pos_vel(
        "1 25544U 98067A   22308.86337963  .00016735  00000+0  30304-3 0  9994",
        "2 25544  51.6449 359.6935 0006351  41.3591 303.6163 15.49753126366997",
        datetime)
    print(ECI_TO_ITRS(teme, datetime))

if __name__ == "__main__":
    main()