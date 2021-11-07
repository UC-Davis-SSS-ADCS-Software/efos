import numpy as np

def Quaternions2EulerAngles(q0123):

    q0 = q0123[0,:]
    q1 = q0123[1,:]
    q2 = q0123[2,:]
    q3 = q0123[3,:]

    ptp = np.empty((4,np.size(q0123,1)))
    ptp[0,:] = np.arctan2(2*(q0*q1+q2*q3),1-2*(np.power(q1,2)+np.power(q2,2)))
    ptp[1,:] = np.arcsin(2*(q0*q2-q3*q1))
    ptp[2,:] = np.arctan2(2*(q0*q3+q1*q2),1-2*(np.power(q2,2)+np.power(q3,2)))

    ptp = np.real(ptp)

    return ptp
