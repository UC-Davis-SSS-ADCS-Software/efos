import numpy as np

# Function for mapping quaternion to DCM
def TIBquat(q0123):

    q0 = q0123[0]
    q1 = q0123[1]
    q2 = q0123[2]
    q3 = q0123[3]

    q0_sq = np.power(q0, 2)
    q1_sq = np.power(q1, 2)
    q2_sq = np.power(q2, 2)
    q3_sq = np.power(q3, 2)

    R = np.array([
        [(q0_sq+q1_sq-q2_sq-q3_sq), 2*(q1*q2-q0*q3), 2*(q0*q2+q1*q3)],
        [2*(q1*q2+q0*q3), (q0_sq-q1_sq+q2_sq-q3_sq), 2*(q2*q3-q0*q1)],
        [2*(q1*q3-q0*q2), 2*(q0*q1+q2*q3), (q0_sq-q1_sq-q2_sq+q3_sq)]
    ])

    return R