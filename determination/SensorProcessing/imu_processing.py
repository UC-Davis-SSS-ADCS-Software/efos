# imu processing
# imports
import numpy as np
from ADCS_Constants import GYRO_GAIN, GYRO_FILTER, GYRO_OFFSET, GYRO_ROTATION

# INPUTS: w_x, w_y, w_z at t = t
#         w_x0, w_y0, w_z0  at t = t-1
#         delta_t = time increment
# OUTPUTS: w_measured = [w_x, w_y, w_z] rotation in body frame
def imu_processing(w_x, w_y, w_z, w_x0, w_y0, w_z0, delta_t):
    try:
        w_x = float(w_x)
        w_y = float(w_y)
        w_z = float(w_z)
        w_x0 = float(w_x0)
        w_y0 = float(w_y0)
        w_z0 = float(w_z0)
    except:
        return([np.inf, np.inf, np.inf])
    w_current = np.array((w_x, w_y, w_z))
    w_prev = np.array((w_x0, w_y0, w_z0))
    alpha = np.exp(-1*GYRO_FILTER/delta_t) # value tbd
    w_calib = np.multiply(np.subtract(w_current, GYRO_OFFSET), GYRO_GAIN) # apply offsets and gains
    w_filtered = np.add(np.multiply(w_calib, alpha), np.multiply(w_prev, 1-alpha)) # apply low-pass filter
    w_measured = np.dot(GYRO_ROTATION,w_filtered) # apply rotation matrix
    return w_measured
