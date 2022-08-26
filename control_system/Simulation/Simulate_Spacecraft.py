# Simulate_Spacecraft.py
# Main script for spacecraft simulation with PD control

# Import packages
import numpy as np
import math
import matplotlib.pyplot as plt
from Spacecraft_Dynamics import spacecraft_dynamics
from control_system.Simulation import Attitude_Controller
from EulerAngles2Quaternions import EulerAngles2Quaternions
from Quaternions2EulerAngles import Quaternions2EulerAngles
import time
import datetime
from sgp4.api import Satrec
from target_calc import target_calc

# Define function to calculate position and velocity in GCRS Frame
def GCRS_position(jd, fr):
    e, r, v = satellite.sgp4(jd, fr)
    return np.array([r])

def GCRS_velocity(jd, fr):
    e, r, v = satellite.sgp4(jd, fr)
    return np.array([v])

# Initial time
t0 = time.process_time()

# Input orbit data using TLE (Two-line element set) format for SGP4
s = '1 25544U 98067A   21364.58225513  .00006501  00000-0  12261-3 0  9994'
t = '2 25544  51.6441 91.5424 0004841  342.0852  149.8473 15.49806377319031'
satellite = Satrec.twoline2rv(s, t)

# Simulation of Satellite
print("Simulation Started.")

# Initial conditions for attitude and angular velocity
phi0 = 0
theta0 = 0
psi0 = np.radians(10)
ptp0 = np.array([phi0,theta0,psi0])
q0123_0 = EulerAngles2Quaternions(ptp0)
q_0 = q0123_0[0]
q_1 = q0123_0[1]
q_2 = q0123_0[2]
q_3 = q0123_0[3]
omega1_0 = 0
omega2_0 = 0
omega3_0 = np.radians(5)
omegaRW1_0 = 0
omegaRW2_0 = 0
omegaRW3_0 = 0
state = np.array([q_0,q_1,q_2,q_3,omega1_0,omega2_0,omega3_0,omegaRW1_0,omegaRW2_0,omegaRW3_0],dtype='float') # initial state

# Time window
tfinal = 1000 #sec
timestep = 0.01 #sec
tout = np.arange(0,tfinal+timestep,timestep)
stateout = np.zeros((len(tout),len(state)))

jd_start, fr_start = 2459580, 0.50000
date_start = datetime.datetime(2022,1,12,0,0) # start date needs to match julian date
start_value = jd_start + fr_start
timestep_min = timestep/60   # timestep in minutes
timestep_days = timestep_min/1440 # convert timestep to days
steps = len(tout)
jd_values = np.zeros(int(steps))
fr_values = np.zeros(int(steps))
position = np.zeros([int(steps),3])
velocity = np.zeros([int(steps),3])
date = date_start

# Target attitude quaternion and angular rate
#q_target = np.array([1,0,0,0])
omega_target = np.array([0,0,0])

# Create array to save target quaternion values
q_target_array = np.empty((4,len(tout)))

# Loop through time and integrate
Next = 1
lastPrint = 0
for i in range(len(tout)):
    # Save the current state
    stateout[i,:] = state
    q_measured = state[0:4]
    omega_measured = state[4:7]

    if tout[i] > lastPrint:
        print("Time = ", str(tout[i]), " out of ", str(tfinal))
        lastPrint = lastPrint + Next

    # Calculate ECI position and velocity using SGP4
    temp = start_value + i*timestep_days
    fr_values[i], jd_values[i] = math.modf(temp)
    time_change = datetime.timedelta(minutes=timestep)
    date = date + time_change
    position[i,:] = GCRS_position(jd_values[i],fr_values[i])
    velocity[i,:] = GCRS_velocity(jd_values[i],fr_values[i])

    # Calculate target quaternion
    q_target = target_calc(position[i,:])
    q_target_array[:,i] = q_target

    # Create Attitude Control object using state vector
    attitude_control_object = Attitude_Controller.Attitude_Control(q_target, q_measured, omega_target, omega_measured)

    # Calculate Control Torque using Attitude Controller
    control_torque = attitude_control_object.attitude_control()
    #print(control_torque)
    #control_torque = np.array([0,0,0],dtype='float')
    #control_torque = np.array([control_torque[0],0,0],dtype='float')    # can only control torque on x-axis

    # 4th Order Runge-Kutta Integrator
    k1 = spacecraft_dynamics(tout[i],state,control_torque)
    k2 = spacecraft_dynamics(tout[i]+timestep/2,state+k1*timestep/2,control_torque)
    k3 = spacecraft_dynamics(tout[i]+timestep/2,state+k2*timestep/2,control_torque)
    k4 = spacecraft_dynamics(tout[i]+timestep,state+k3*timestep,control_torque)
    k = (1.0/6.0)*(k1+2*k2+2*k3+k4)
    state = state + k*timestep

print("Simulation Complete.")

# Extract the state vectors
q0123out = np.empty((4,len(tout)))
q0123out[0] = stateout[:,0]
q0123out[1] = stateout[:,1]
q0123out[2] = stateout[:,2]
q0123out[3] = stateout[:,3]
ptpout = Quaternions2EulerAngles(q0123out)
omegaout = np.empty((3,len(tout)))
omegaout[0] = stateout[:,4]
omegaout[1] = stateout[:,5]
omegaout[2] = stateout[:,6]

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

# Compute target euler angles
euler_target = Quaternions2EulerAngles(q_target_array)

# Plot Euler Angles
plt.plot(tout, np.degrees(ptpout[0]), color='b', linewidth=2, label='Roll')
plt.plot(tout, np.degrees(ptpout[1]), color='g', linewidth=2, label='Pitch')
plt.plot(tout, np.degrees(ptpout[2]), color='r', linewidth=2, label='Yaw')
plt.plot(tout, np.degrees(euler_target[0]), color='b', linewidth=2, label='Roll Target', linestyle='--')
plt.plot(tout, np.degrees(euler_target[1]), color='g', linewidth=2, label='Pitch Target', linestyle='--')
plt.plot(tout, np.degrees(euler_target[2]), color='r', linewidth=2, label='Yaw Target', linestyle='--')
plt.xlabel('Time (sec)')
plt.ylabel('Angles (degrees)')
plt.title('Euler Angles')
plt.legend()
plt.grid(True)
plt.show()

# Plot Angular Velocity
plt.plot(tout, np.degrees(omegaout[0]), color='b', linewidth=2, label='Roll Rate')
plt.plot(tout, np.degrees(omegaout[1]), color='g', linewidth=2, label='Pitch Rate')
plt.plot(tout, np.degrees(omegaout[2]), color='r', linewidth=2, label='Yaw Rate')
plt.xlabel('Time (sec)')
plt.ylabel('Angular Velocity (degrees/s)')
plt.title('Angular Velocity')
plt.legend()
plt.grid(True)
plt.show()

# Final time
t1 = time.process_time()-t0
print("Time elapsed (min): ", t1/60)