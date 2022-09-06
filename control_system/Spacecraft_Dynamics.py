# Spacecraft_Dynamics.py
# Simulate CubeSat dynamics over orbit
# Input: time, state, control torque

# Import Python packages
import numpy as np
import matplotlib as plt
from numpy.linalg import inv
from numpy.linalg import solve

# Define skew function
def Skew(v):
    S = np.array([
        [0, -1*v[2], v[1]],
        [v[2], 0, -1*v[0]],
        [-1*v[1], v[0], 0]
    ],dtype=object)
    return S

# Define function
def spacecraft_dynamics(t, state, control_torque):
    # Extract states
    q0 = state[0]
    q1 = state[1]
    q2 = state[2]
    q3 = state[3]
    q_state = np.array([q0,q1,q2,q3],dtype='float')
    omega1 = state[4]
    omega2 = state[5]
    omega3 = state[6]
    omega_state = np.array([omega1,omega2,omega3],dtype='float')
    omegaRW1 = state[7]
    omegaRW2 = state[8]
    omegaRW3 = state[9]
    omegaRW_state = np.array([omegaRW1,omegaRW2,omegaRW3],dtype='float')

    # System parameters
    J = np.array([  # inertia matrix for CubeSat
        [8393796.35, -3899.99, 4177.60],
        [-3899.99, 7998727.19, 12703.44],
        [4177.60, 12703.44, 4335966.23]
    ],dtype='float')

    J = J*(1e-3)*(1e-3)**2 # convert to kg*m^2

    # Inertia matrix and mass for reaction wheel
    # Currently estimated parameters need real parameters from
    # MRW Team
    J_RW = np.array([
        [11499.76, 0, 0],
        [0, 11499.76, 0],
        [0, 0, 22908.71]
    ],dtype='float')

    J_RW = J_RW*(1e-3)*(1e-3)**2 # convert to kg*m^2

    M_RW = 60.54e-3 # kg

    # Translational Dynamics
    ## Add sgp4.py package to simulate orbit

    # Angular Kinematics
    # Propagate attitude quaternion
    Omega = np.array([
        [0, -1*omega1, -1*omega2, -1*omega3],
        [omega1, 0, omega3, -1*omega2],
        [omega2, -1*omega3, 0, omega1],
        [omega3, omega2, -1*omega1, 0]
    ],dtype='float')

    q_dot = 0.5*np.dot(Omega,q_state)

    # Propagate angular rotation rates
    torque = np.array([0,0,0+control_torque[2]],dtype='float')
    H_sc = np.dot(J,omega_state)
    H_RW = np.dot(J_RW,omegaRW_state)
    temp_matrix = np.add(np.subtract(np.dot(Skew(omega_state),H_sc), torque), np.dot(Skew(omega_state),H_RW))
    if np.abs(temp_matrix[0]) < 1e-5 or np.abs(temp_matrix[0] == np.NaN):
        temp_matrix[0] = 0
    if np.abs(temp_matrix[1]) < 1e-5 or np.abs(temp_matrix[1] == np.NaN):
        temp_matrix[1] = 0
    if np.abs(temp_matrix[2]) < 1e-5 or np.abs(temp_matrix[2] == np.NaN):
        temp_matrix[2] = 0
    omega_dot = solve(-1*J,np.array([temp_matrix[0],temp_matrix[1],temp_matrix[2]],dtype='float'))
    #omega_dot = np.dot(-1*inv(J),np.array([temp_matrix[0],temp_matrix[1],temp_matrix[2]],dtype='float'))

    # Propagate Reaction Wheel angular rotation rates
    omegaRW1_dot = 0
    omegaRW2_dot = 0
    omegaRW3_dot = control_torque[2]/J_RW[2,2] 

    # Return derivatives vector
    dstatedt = np.empty((10,))
    dstatedt[0] = q_dot[0]
    dstatedt[1] = q_dot[1]
    dstatedt[2] = q_dot[2]
    dstatedt[3] = q_dot[3]
    dstatedt[4] = omega_dot[0]
    dstatedt[5] = omega_dot[1]
    dstatedt[6] = omega_dot[2]
    dstatedt[7] = omegaRW1_dot
    dstatedt[8] = omegaRW2_dot
    dstatedt[9] = omegaRW3_dot
    return dstatedt