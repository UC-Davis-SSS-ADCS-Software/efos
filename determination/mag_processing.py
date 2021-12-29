# mag processing
# imports
import numpy as np
import matplotlib.pyplot as plt

# constants
mag_wc = 0.40 # tbd
mag_gain = 1.0
mag_offset = 0.0


# INPUTS: m_current = [m_x, m_y, m_z] at t = t
#         m_prev = [m_x, m_y, m_z]  at t = t-1
#         delta_t = time increment
# OUTPUTS: m_filtered = [m_x, m_y, m_z] with gains, offsets, filtering applied
def mag_processing(m_current, m_prev, delta_t):
    alpha = np.exp(-1*mag_wc/delta_t) # value tbd
    m_calib = [x - mag_offset for x in m_current] # apply offfsets
    m_calib = np.multiply(m_calib, mag_gain) # apply gains
    m_filtered = np.add(np.multiply(m_calib, alpha), np.multiply(m_prev, 1-alpha)) # apply low-pass filter
    return m_filtered
