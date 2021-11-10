# Test of SGP4 Orbit Propagator
# Compute x,y,z position and velocity for ISS at 12:50:19 on 29 June 2000

from sgp4.api import Satrec

# Input orbit data using TLE (Two-line element set) format
s = '1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9991'
t = '2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482'
satellite = Satrec.twoline2rv(s, t)

jd, fr = 2458827, 0.362605
e, r, v = satellite.sgp4(jd, fr)

print(r)  # True Equator Mean Equinox position (km)
print(v)  # True Equator Mean Equinox velocity (km/s)