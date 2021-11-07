# DCM between NED frame and ECI frame
import numpy as np

def TIB(phi,theta,psi):
    ct = np.cos(theta)
    st = np.sin(theta)
    sp = np.sin(phi)
    cp = np.cos(phi)
    ss = np.sin(psi)
    cs = np.cos(psi)

    T = np.array([
        [ct*cs, sp*st*cs-cp*ss, cp*st*cs+sp*ss],
        [ct*ss, sp*st*ss+cp*cs, cp*st*ss-sp*cs],
        [-st, sp*ct, cp*ct]
    ])

    return T