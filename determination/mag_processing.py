# mag processing
# imports
# notes: 
# * mag_wc can change depending on how much filtering we want (and depending on sampling rate)
# * currently sampling rate is 200ms, will check with cs how often we will sample data from magnetometer
# * still need rotation matrix depending on imu location in cubesat
import numpy as np
import matplotlib.pyplot as plt
# constants
mag_wc = 0.15 # tbd
mag_gain = np.array((1.0,1.0,1.0)) # from hardware testing
mag_offset = np.array((0,0,0)) # from hardware testing

# INPUTS: m_x, m_y, m_z: raw magnetomer t = t
#         m_x0, m_y0, m_z0: filtered magnetometer data at t = t-1
#         delta_t = time increment
#         r = rotation matrix from sensor frame to body frame
# OUTPUTS: b_body = [m_x, m_y, m_z] magnetic field in body frame
def mag_processing(m_x, m_y, m_z, m_x0, m_y0, m_z0, delta_t, r):
    try:
        m_x = float(m_x)
        m_y = float(m_y)
        m_z = float(m_z)
        m_x0 = float(m_x0)
        m_y0 = float(m_y0)
        m_z0 = float(m_z0)
    except:
        return([np.inf, np.inf, np.inf])
    m_current = np.array((m_x, m_y, m_z))
    m_prev = np.array((m_x0, m_y0, m_z0))
    alpha = np.exp(-1*mag_wc/delta_t) # value tbd
    m_calib = np.multiply(np.subtract(m_current, mag_offset), mag_gain) # apply offsets and gains
    m_filtered = np.add(np.multiply(m_calib, alpha), np.multiply(m_prev, 1-alpha)) # apply low-pass filter
    b_body = np.dot(r,m_filtered) # apply rotation matrix
    return b_body
