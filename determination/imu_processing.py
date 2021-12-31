# imu processing
# imports
import numpy as np

# constants
gyro_wc = 0.40 # tbd
gyro_gain = np.array((1.0,1.0,1.0)) # from hardware testing
gyro_offset = np.array((0,0,0)) # from hardware testing

# INPUTS: w_x, w_y, w_z at t = t
#         w_x0, w_y0, w_z0  at t = t-1
#         delta_t = time increment
#         r = rotation matrix from sensor frame to body frame
# OUTPUTS: w_measured = [w_x, w_y, w_z] rotation in body frame
def mag_processing(w_x, w_y, w_z, w_x0, w_y0, w_z0, delta_t, r):
    w_current = np.array((w_x, w_y, w_z))
    w_prev = np.array((w_x0, w_y0, w_z0))
    alpha = np.exp(-1*gyro_wc/delta_t) # value tbd
    w_calib = np.multiply(np.subtract(w_current, gyro_offset), gyro_gain) # apply offsets and gains
    w_filtered = np.add(np.multiply(w_calib, alpha), np.multiply(w_prev, 1-alpha)) # apply low-pass filter
    w_measured = np.dot(r,w_filtered) # apply rotation matrix
    return w_measured
