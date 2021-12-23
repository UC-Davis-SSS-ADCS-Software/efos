import numpy as np

def Quaternions2EulerAngles(q0123):

    q0 = q0123[0,:]
    q1 = q0123[1,:]
    q2 = q0123[2,:]
    q3 = q0123[3,:]

    ptp = np.empty((4,np.size(q0123,1)))
    ptp[0,:] = np.arctan2(2*(q0*q1+q2*q3),1-2*(np.power(q1,2)+np.power(q2,2)))
    for i in range(len(q0123[0,:])):
        if np.abs(2*(q0[i]*q2[i]-q3[i]*q1[i])) < 1:
            ptp[1,i] = np.arcsin(2*(q0[i]*q2[i]-q3[i]*q1[i]))
        else:
            norm = np.sqrt(q0[i]**2 + q1[i]**2 + q2[i]**2 + q3[i]**2)
            q0n = q0[i]/norm
            q1n = q1[i]/norm
            q2n = q2[i]/norm
            q3n = q3[i]/norm
            ptp[1,i] = np.arcsin(2*(q0n*q2n-q3n*q1n))
    ptp[2,:] = np.arctan2(2*(q0*q3+q1*q2),1-2*(np.power(q2,2)+np.power(q3,2)))

    ptp = np.real(ptp)

    return ptp
