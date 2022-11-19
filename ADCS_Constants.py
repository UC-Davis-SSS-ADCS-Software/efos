import numpy as np

# SUN SENSORS (all values need hardware testing)
ECLIPSE_THRESHOLD = 0 # lower limit for a sun diode to be considered "in the dark"
SUN_OFFSET = np.zeros(24) # diode calibration offsets
SUN_GAIN = np.ones(24) # diode calibration offsets
SUN_FILTER = 0.20 # sun low-pass filter time constant

# IMU calibration constants
MAG_OFFSET = [0, 0, 0] # magnetometer calibration offsets
MAG_GAIN = [1, 1, 1] # magnetometer gain offsets
MAG_FILTER = 0.15 # magnetometer filter time constant
GYRO_OFFSET = [0, 0, 0] # gyroscope calibration offsets
GYRO_GAIN = [1, 1, 1] # gyroscope gain offsets
GYRO_FILTER = 0.40 # gyro filter time constant

# REFERENCE ANGLES
THETA_IMU = 90  # degrees; angle from IMU to body frame, measured CCW
R = np.array(((np.cos(THETA_IMU), -np.sin(THETA_IMU), 0), (np.sin(THETA_IMU), np.cos(THETA_IMU), 0), (0, 0, 1))) # Rotation matrix to aign IMU and Satellite Axes

# CONTROLLER CONSTANTS (PID needs hardware testing)
BDOT_GAIN = 67200 # bdot gain constant when bdot is on
PROP_CONTROL_MRW = 1 # PID KP when RW is on (MRW)
INTEGRAL_CONTROL_MRW = 1 # PID KI when RW is on (MRW)
DERIVATIVE_CONTROL_MRW = 1 # PID KD when RW is on (MRW)
PROP_CONTROL_HDD = 1 # PID KP when RW is on (HDD)
INTEGRAL_CONTROL_HDD = 1 # PID KI when RW is on (HDD)
DERIVATIVE_CONTROL_HDD = 1 # PID KD when RW is on (HDD)

# MRW CONSTANTS
MAX_RW_ANGVEL = 4188.0  # max MRW speed (need to verify w/ hardware testing)
MAX_TORQUE = 10 # max MRW torque, need to calculate with hardware testing
RW_MOI = 0.00002353 # MRW moment of inertia (kg * m2)
J_CS = 1 # cubesat moment of inertia (need to get from Structures)

# OTHER CONSTANTS
# TODO check if CS sets the IMU thresholds or if we need to check for them
IMU_THRESH = [0, 0, 0] # threshold for detumbling in rad/s
