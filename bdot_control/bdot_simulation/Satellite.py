import numpy as np
import pyIGRF
from TIB import TIB
from TIBquat import TIBquat
from Control import Control
from Sensor import Sensor
import globals

# Planet parameters
R = 6.371e6 # radius of earth in meters
M = 5.972e24 # mass of earth in kg
G = 6.67e-11 # gravitational constant in SI units
mu = G*M

altitude = 600 # kilometers

def Satellite(t, state):

    x = state[0]
    y = state[1]
    z = state[2]
    q0 = state[6]
    q1 = state[7]
    q2 = state[8]
    q3 = state[9]
    q0123 = np.array([q0,q1,q2,q3])
    p = state[10]
    q = state[11]
    r = state[12]
    pqr = np.array([p,q,r])


    # intertia and mass
    m = globals.m # kg
    I = globals.I #kg-m^2
    invI = globals.invI

    # Translational Kinematics
    vel = np.array([state[3],state[4],state[5]])

    # Rotational Kinematics
    PQRMAT = np.array([
        [0, -p, -q, -r],
        [p, 0, r, -q],
        [q, -r, 0, p],
        [r, q, -p, 0]
    ])
    q0123dot = 0.5*np.dot(PQRMAT, q0123)

    # Gravity model
    r_st = np.array([state[0],state[1],state[2]]) # r = [x,y,z]
    rho = np.linalg.norm(r_st)
    rhat = np.divide(r_st,rho)
    Fgrav = -(G*M*m/np.power(rho,2))*rhat

    # Magnetic field model (pyIGRF)
    phiE = 0
    thetaE = np.arccos(z/rho)
    psiE = np.arctan2(y,x)
    latitude = 90-thetaE*180/np.pi
    longitude = psiE*180/np.pi
    igrf_output = pyIGRF.igrf_value(latitude, longitude, altitude, 	2020)
    BN = igrf_output[3]
    BE = igrf_output[4]
    BD = igrf_output[5]
    BNED = np.array([BN,BE,BD])
    # Transform to ECI frame
    BI = np.dot(TIB(phiE, thetaE+np.pi, psiE), BNED)
    BB = np.dot(TIBquat(q0123),BI) * 1e-9
    globals.BB = BB

    # magnetorquer parameters
    n_aircore = 195 # turns
    n_rods = 440 # turns
    A_aircore = 0.006084 # m^2
    A_rod = 0.0001423 # m^2
    nA = np.array([n_rods*A_rod, n_rods*A_rod, n_aircore*A_aircore])

    # Sensor Block
    if t > globals.lastSensorUpdate or t==0:
        globals.lastSensorUpdate = globals.lastSensorUpdate + globals.nextSensorUpdate
        sensor_output = Sensor(BB, pqr)
        globals.BfieldMeasured = np.array([sensor_output[0,0], sensor_output[0,1], sensor_output[0,2]])
        globals.pqrMeasured = np.array([sensor_output[1,0], sensor_output[1,1], sensor_output[1,2]])

    BBm = globals.BfieldMeasured
    pqrm = globals.pqrMeasured

    # Control Block
    current = Control(BBm, pqrm)
    muB = np.array([current[0]*nA[0], current[1]*nA[1], current[2]*nA[2]])
    globals.current = current

    # Magnetorquer Model
    LMN_magtorquers = np.cross(muB,BBm)

    # Translational Dynamics
    F = Fgrav
    accel = np.divide(F,m)

    # Rotational Dynamics
    H = np.dot(I,pqr)
    pqrdot = np.dot(invI,(LMN_magtorquers - np.cross(pqr,H)))

    # Return derivatives vector
    dstatedt = np.empty((13,))
    dstatedt[0] = vel[0]
    dstatedt[1] = vel[1]
    dstatedt[2] = vel[2]
    dstatedt[3] = accel[0]
    dstatedt[4] = accel[1]
    dstatedt[5] = accel[2]
    dstatedt[6] = q0123dot[0]
    dstatedt[7] = q0123dot[1]
    dstatedt[8] = q0123dot[2]
    dstatedt[9] = q0123dot[3]
    dstatedt[10] = pqrdot[0]
    dstatedt[11] = pqrdot[1]
    dstatedt[12] = pqrdot[2]
    return dstatedt
