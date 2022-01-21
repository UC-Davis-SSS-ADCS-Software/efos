# SGP4 Plot of ISS Orbit

# Import packages
import numpy as np
import math
from sgp4.api import Satrec
#import skyfield.sgp4lib as sgp4lib
import datetime
#from astropy import coordinates as coord, units as u
#from astropy.time import Time
import matplotlib.pyplot as plt
import csv

# Define function to calculate position and velocity in GCRS Frame
def GCRS_position_velocity(jd, fr, date):
    e, r, v = satellite.sgp4(jd, fr)
    #time = jd + fr

    # Convert from TEME to ITRS frame (v must be in units of km/day so we mulitply be 86400)
    #r_prime,v_prime = sgp4lib.TEME_to_ITRF(time,np.asarray(r),np.asarray(v)*86400)
    #v_prime = v_prime/86400 # convert v_prime from km/day to km/s

    # Convert from ITRS to GCRS ECI frame
    #current_time = Time(date)
    #itrs = coord.ITRS(r_prime[0]*u.km,r_prime[1]*u.km,r_prime[2]*u.km,v_prime[0]*u.km/u.s,v_prime[1]*u.km/u.s,v_prime[2]*u.km/u.s,obstime=current_time)
    #gcrs = itrs.transform_to(coord.GCRS(obstime=current_time))
    #r_ECI,v_ECI = gcrs.cartesian.xyz.value,gcrs.velocity.d_xyz.value

    #return np.array([r_ECI,v_ECI])
    return np.array([r])

# Input orbit data using TLE (Two-line element set) format
s = '1 25544U 98067A   21364.58225513  .00006501  00000-0  12261-3 0  9994'
t = '2 25544  51.6441 91.5424 0004841  342.0852  149.8473 15.49806377319031'
satellite = Satrec.twoline2rv(s, t)

# Open CSV file to write data
f = open("orbit_position_data.csv", 'w', newline="")
w = csv.writer(f)

# create csv file headers for data
fields = ['x', 'y', 'z']
w.writerow(fields)

# Fill array of julian dates for input to SGP4
jd_start, fr_start = 2459580, 0.50000
date_start = datetime.datetime(2022,1,12,0,0) # start date needs to match julian date
start_value = jd_start + fr_start
timestep = 1   # timestep in minutes
timestep_days = timestep/1440 # convert timestep to days
steps = 500
jd_values = np.zeros(steps)
fr_values = np.zeros(steps)
position = np.zeros([steps,3])
velocity = np.zeros([steps,3])
date = date_start
for i in range(steps):
    temp = start_value + i*timestep_days
    fr_values[i], jd_values[i] = math.modf(temp)
    time_change = datetime.timedelta(minutes=timestep)
    date = date + time_change
    position[i,:] = GCRS_position_velocity(jd_values[i],fr_values[i],date)
    print(position[i,:])
    w.writerow(position[i,:])

# Make an Earth
R = 6.371e6 # radius of earth in meters

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, projection='3d')

u = np.linspace(0, 2*np.pi, 100)
v = np.linspace(0, np.pi, 100)

X = np.outer(np.cos(u), np.sin(v))
Y = np.outer(np.sin(u), np.sin(v))
Z = np.outer(np.ones(np.size(u)), np.cos(v))
X = X*R/1000
Y = Y*R/1000
Z = Z*R/1000
ax.plot_surface(X,Y,Z, rstride=4, cstride=4, color='b', alpha=0.4)

# Plot 3D orbit
ax.plot3D(position[:,0],position[:,1],position[:,2],label='Simulated Orbit',color='r',linewidth=4)
ax.legend()
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()