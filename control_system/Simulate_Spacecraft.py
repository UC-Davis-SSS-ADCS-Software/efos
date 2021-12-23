# Simulate_Spacecraft.py
# Main script for spacecraft simulation with PD control

# Import packages
import numpy as np
import matplotlib.pyplot as plt
from Spacecraft_Dynamics import spacecraft_dynamics
import Attitude_Controller
from EulerAngles2Quaternions import EulerAngles2Quaternions
from Quaternions2EulerAngles import Quaternions2EulerAngles
import time

# Initial time
t0 = time.process_time()

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
omega3_0 = np.radians(10)
omegaRW1_0 = 0
omegaRW2_0 = 0
omegaRW3_0 = 0
state = np.array([q_0,q_1,q_2,q_3,omega1_0,omega2_0,omega3_0,omegaRW1_0,omegaRW2_0,omegaRW3_0],dtype='float') # initial state

# Time window
tfinal = 100 #sec
timestep = 0.001 #sec
tout = np.arange(0,tfinal+timestep,timestep)
stateout = np.zeros((len(tout),len(state)))

# Target attitude quaternion and angular rate
q_target = np.array([1,0,0,0])
omega_target = np.array([0,0,0])

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

    # Create Attitude Control object using state vector
    attitude_control_object = Attitude_Controller.Attitude_Control(q_target,q_measured,omega_target,omega_measured)

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
print(len(q0123out[0]))
q0123out[1] = stateout[:,1]
q0123out[2] = stateout[:,2]
q0123out[3] = stateout[:,3]
ptpout = Quaternions2EulerAngles(q0123out)
omegaout = np.empty((3,len(tout)))
omegaout[0] = stateout[:,4]
omegaout[1] = stateout[:,5]
omegaout[2] = stateout[:,6]

# Plot Euler Angles
plt.plot(tout, np.degrees(ptpout[0]), color='b', linewidth=2, label='Roll')
plt.plot(tout, np.degrees(ptpout[1]), color='g', linewidth=2, label='Pitch')
plt.plot(tout, np.degrees(ptpout[2]), color='r', linewidth=2, label='Yaw')
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