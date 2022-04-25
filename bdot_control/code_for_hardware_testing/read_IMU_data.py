# Read IMU data from txt file

import numpy as np
from bdot_control import bdot_control

# magnetorquer parameters
n_aircore = 195 # turns
n_rods = 440 # turns
A_aircore = 0.006084 # m^2
A_rod = 0.0001423 # m^2
nA = np.array([n_rods*A_rod, n_rods*A_rod, n_aircore*A_aircore])

# read txt file containing data (include path to txt file in open() function)
with open('Bdot\Code for Hardware Testing\data.txt') as f:
    for line in f:
        split_line = line.split(',')
        omega = np.array([float(split_line[0]),float(split_line[1]),float(split_line[2])])
        mag_field = np.array([float(split_line[3]),float(split_line[4]),float(split_line[5])])*1e-6    # factor of 1e-6 is assuming mag data is in microteslas
        current = bdot_control(mag_field,omega)
        mag_moment = np.array([current[0]*nA[0], current[1]*nA[1], current[2]*nA[2]])
        magnetorquer_torque = np.cross(mag_moment,mag_field)
        print("Current Output:",current,"amps, Expected Magnetorquer Torque:", magnetorquer_torque, "N-m")