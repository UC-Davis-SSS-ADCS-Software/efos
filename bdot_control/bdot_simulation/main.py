### Code adapted from Carlos Jose Montalvo's ADCS Seminar Series
### https://github.com/cmontalvo251/MATLAB/tree/master/ADCS_Seminar_Series

# Import packages
import numpy as np
from scipy import integrate as ode
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from Satellite import Satellite
import globals
from EulerAngles2Quaternions import EulerAngles2Quaternions
from Quaternions2EulerAngles import Quaternions2EulerAngles
import time

# Initial time
t0 = time.clock()

# Simulation of Low Earth Orbit Satellite
print("Simulation Started.")

# Planet parameters
R = 6.371e6 # radius of earth in meters
M = 5.972e24 # mass of earth in kg
G = 6.67e-11 # gravitational constant in SI units
mu = G*M

# mass and inertia properties
m = 2.6 # kilograms
# Inertia in kg-m^2
I = np.array([
    [0.9, 0, 0],
    [0, 0.9, 0],
    [0, 0, 0.3]
])
invI = np.linalg.inv(I)
globals.m = m
globals.I = I
globals.invI = invI

# Initial conditions for position and velocity
altitude = 254*1.609*1000 # 254 mi converted to meters (ISS altitude)
x0 = R + altitude
y0 = 0
z0 = 0
xdot0 = 0
inclination = np.radians(51.6) # ISS orbit inclination angle
semi_major = np.linalg.norm(np.array([x0,y0,z0])) # semi-major axis
vcircular = np.sqrt(mu/semi_major) # orbital speed
ydot0 = vcircular*np.cos(inclination)
zdot0 = vcircular*np.sin(inclination)

# Initial conditions for attitude and angular velocity
phi0 = 0
theta0 = 0
psi0 = 0
ptp0 = np.array([phi0,theta0,psi0])
q0123_0 = EulerAngles2Quaternions(ptp0)
q_0 = q0123_0[0]
q_1 = q0123_0[1]
q_2 = q0123_0[2]
q_3 = q0123_0[3]
p0 = 0.08
q0 = -0.02
r0 = 0.03
state = np.array([x0,y0,z0,xdot0,ydot0,zdot0,q_0,q_1,q_2,q_3,p0,q0,r0]) # initial state vector

# Time window
period = 2*np.pi/np.sqrt(mu)*np.power(semi_major,1.5) # period of orbit
number_of_orbits = 1
tfinal = period*number_of_orbits
timestep = 1
tout = np.arange(0,tfinal+timestep,timestep)
stateout = np.zeros((len(tout),len(state)))

# Sensor parameters
globals.lastSensorUpdate = 0

# Loop through time to integrate
BxBout = 0*stateout[:,0]
ByBout = 0*BxBout
BzBout = 0*BxBout
BxBm = 0*BxBout
ByBm = 0*BxBout
BzBm = 0*BxBout
pqrm = np.array([0*BxBout, 0*BxBout, 0*BxBout])
currentx = 0*BxBout
currenty = 0*BxBout
currentz = 0*BxBout
Next = 100
lastPrint = 0
for i in range(len(tout)):
    # Save the current state
    stateout[i,:] = state

    if tout[i] > lastPrint:
        print("Time = ", str(tout[i]), " out of ", str(tfinal))
        lastPrint = lastPrint + Next

    # 4th Order Runge-Kutta Integrator
    k1 = Satellite(tout[i],state)
    k2 = Satellite(tout[i]+timestep/2,state+k1*timestep/2)
    k3 = Satellite(tout[i]+timestep/2,state+k2*timestep/2)
    k4 = Satellite(tout[i]+timestep,state+k3*timestep)
    k = (1.0/6.0)*(k1+2*k2+2*k3+k4)
    state = state + k*timestep

    # Save magnetic field
    BxBout[i] = globals.BB[0]
    ByBout[i] = globals.BB[1]
    BzBout[i] = globals.BB[2]

    # Save current
    currentx[i] = globals.current[0]
    currenty[i] = globals.current[1]
    currentz[i] = globals.current[2]

    # Save polluted data
    BxBm[i] = globals.BfieldMeasured[0]
    ByBm[i] = globals.BfieldMeasured[1]
    BzBm[i] = globals.BfieldMeasured[2]
    pqrm[:, i] = globals.pqrMeasured

print("Simulation Complete.")

# Convert to km
stateout[:,0:5] = stateout[:,0:5]/1000
x = stateout[:,0]
y = stateout[:,1]
z = stateout[:,2]

# Extract the state vectors
q0123out = np.empty((4,len(tout)))
q0123out[0] = stateout[:,6]
q0123out[1] = stateout[:,7]
q0123out[2] = stateout[:,8]
q0123out[3] = stateout[:,9]
ptpout = Quaternions2EulerAngles(q0123out)
pqrout = np.empty((3,len(tout)))
pqrout[0] = stateout[:,10]
pqrout[1] = stateout[:,11]
pqrout[2] = stateout[:,12]

# Plot position as function of time
plt.plot(tout, x, color='b', linewidth=2, label='X')
plt.plot(tout, y, color='g', linewidth=2, label='Y')
plt.plot(tout, z, color='r', linewidth=2, label='Z')
plt.xlabel('Time (sec)')
plt.ylabel('Position (meters)')
plt.title('Satellite Position in ECI Frame')
plt.legend()
plt.grid(True)
plt.show()


# Make an Earth
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
ax.plot3D(x, y, z, label='Simulated Orbit', color='r', linewidth=4)
ax.legend()
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()

# Plot magnetic field
plt.plot(tout, BxBout, color='b', linewidth=2, label='X True')
plt.plot(tout, ByBout, color='r', linewidth=2, label='Y True')
plt.plot(tout, BzBout, color='g', linewidth=2, label='Z True')
plt.plot(tout, BxBm, color='b', linestyle = 'dashed', linewidth=2, label='X Measured')
plt.plot(tout, ByBm, color='r', linestyle = 'dashed', linewidth=2, label='Y Measured')
plt.plot(tout, BzBm, color='g', linestyle = 'dashed', linewidth=2, label='Z Measured')
plt.xlabel('Time (sec)')
plt.ylabel('Magnetic Field (T)')
plt.title('Magnetic Field Strength in Body Frame Coordinates')
plt.legend()
plt.grid(True)
plt.show()

# Plot Euler Angles
plt.plot(tout, ptpout[0], color='b', linewidth=2, label='Roll')
plt.plot(tout, ptpout[1], color='g', linewidth=2, label='Pitch')
plt.plot(tout, ptpout[2], color='r', linewidth=2, label='Yaw')
plt.xlabel('Time (sec)')
plt.ylabel('Angles (rad)')
plt.title('Euler Angles')
plt.legend()
plt.grid(True)
plt.show()

# Plot Angular Velocity
plt.plot(tout/period, pqrout[0], color='b', linewidth=2, label='Roll Rate True')
plt.plot(tout/period, pqrout[1], color='g', linewidth=2, label='Pitch Rate True')
plt.plot(tout/period, pqrout[2], color='r', linewidth=2, label='Yaw Rate True')
plt.plot(tout/period, pqrm[0], color='b', linestyle = 'dashed', linewidth=2, label='Roll Rate Measured')
plt.plot(tout/period, pqrm[1], color='g', linestyle = 'dashed', linewidth=2, label='Pitch Rate Measured')
plt.plot(tout/period, pqrm[2], color='r', linestyle = 'dashed', linewidth=2, label='Yaw Rate Measured')
plt.xlabel('Number of Orbits', fontsize=22)
plt.ylabel('Angular Velocity (rad/s)', fontsize=22)
plt.title('Angular Velocity', fontsize=36)
plt.legend(fontsize=20)
plt.grid(True)
plt.show()

# Plot power over time
airecore_resistance = 13.89 # ohms
rod_resistance = 13.89 # ohms
powerx = np.power(currentx,2)*rod_resistance
powery = np.power(currenty,2)*rod_resistance
powerz = np.power(currentz,2)*airecore_resistance
plt.plot(tout/(60*60), powerx, color='b', linewidth=2, label='Power Usage due to Magnetorquer in x-axis')
plt.plot(tout/(60*60), powery, color='g', linewidth=2, label='Power Usage due to Magnetorquer in y-axis')
plt.plot(tout/(60*60), powerz, color='r', linewidth=2, label='Power Usage due to Magnetorquer in z-axis')
plt.xlabel('Time (hours)', fontsize=22)
plt.ylabel('Power Usage (W)', fontsize=22)
plt.title("Power Usage during Detumbling", fontsize=36)
plt.legend(fontsize=20)
plt.grid(True)
plt.show()

check = 0
counter = 0
for i in range(len(pqrout[0])):
    if ((pqrout[0,i] < np.radians(0.5)) and (pqrout[1,i] < np.radians(0.5)) and (pqrout[2,i] < np.radians(0.5))):
        counter = counter + 1
        if counter > 100:
            print("Number of orbits to get under 0.5 deg/sec", tout[i-100]/period)
            check = check + 1
            break
if check == 0:
    print("No values under 0.5 deg/sec")

print("Max Power Used for x-axis: ", np.amax(powerx))
print("Max Power Used for y-axis: ", np.amax(powery))
print("Max Power Used for z-axis: ", np.amax(powerz))

# Final time
t1 = time.clock()-t0
print("Time elapsed (min): ", t1/60)