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