# Test TLE_to_pos_vel
from TLE_to_pos_vel import TLE_to_pos_vel, parse_time

s = '1 25544U 98067A   21364.58225513  .00006501  00000-0  12261-3 0  9994'
t = '2 25544  51.6441 91.5424 0004841  342.0852  149.8473 15.49806377319031'
datetime = '2022,4,6,14,30,30'
print(parse_time(datetime))
print(TLE_to_pos_vel(s,t,datetime))