# Script to calculate Kp and Kd gains for PD Controller (from Adam Zufall)
# Given inertia matrix, damping ratio, rise time -> return Kp,Kd
import numpy as np

def calc_gains(J,zeta,rise_time):
    Jxx = J[0,0]
    Jyy = J[1,1]
    Jzz = J[2,2]

    gain_margin = 1.5

    wn = (np.pi - np.arctan2(np.sqrt(1-zeta**2),zeta))/(rise_time*np.sqrt(1-zeta**2)) # natural frequency

    Kpx = gain_margin*Jxx*wn**2
    Kpy = gain_margin*Jyy*wn**2
    Kpz = gain_margin*Jzz*wn**2

    Kdx = 2*gain_margin*zeta*Jxx*wn
    Kdy = 2*gain_margin*zeta*Jyy*wn
    Kdz = 2*gain_margin*zeta*Jzz*wn

    return np.array([Kpx,Kpy,Kpz,Kdx,Kdy,Kdz])

J = np.array([  # inertia matrix for CubeSat
        [8393796.35, -3899.99, 4177.60],
        [-3899.99, 7998727.19, 12703.44],
        [4177.60, 12703.44, 4335966.23]
    ],dtype='float')

J = J*(1e-3)*(1e-3)**2 # convert to kg*m^2

gains = calc_gains(J,0.5,2)
Kp = gains[0:3]
Kd = gains[3:6]
print(Kp)
print(Kd)