# Target Calculation

import numpy as np

# Define skew function
def Skew(v):
    S = np.array([
        [0, -1*v[2], v[1]],
        [v[2], 0, -1*v[0]],
        [-1*v[1], v[0], 0]
    ],dtype=object)
    return S

def dcm_to_euler(dcm):
    # Verify DCM is valid
    err = np.linalg.norm(np.identity(3, dtype=dcm.dtype) - np.dot(dcm.T, dcm))
    if err > 1e-3:
        raise InvalidDirectionCosineMatrix
    
    # Map DCM to quaternion components using Sheppard's method
    # determine largest value of squared components
    q_0_sq = 0.25*(1+np.trace(dcm))
    q_1_sq = 0.25*(1+2*dcm[0,0]-np.trace(dcm))
    q_2_sq = 0.25*(1+2*dcm[1,1]-np.trace(dcm))
    q_3_sq = 0.25*(1+2*dcm[2,2]-np.trace(dcm))

    q_sq = [q_0_sq, q_1_sq, q_2_sq, q_3_sq]

    # solve for remaining components using largest component
    if max(q_sq) == q_0_sq:
        q_0 = np.sqrt(q_0_sq)
        q_1 = (dcm[2,1] - dcm[1,2])/(4*q_0)
        q_2 = (dcm[0,2] - dcm[2,0])/(4*q_0)
        q_3 = (dcm[1,0] - dcm[0,1])/(4*q_0)
    elif max(q_sq) == q_1_sq:
        q_1 = np.sqrt(q_1_sq)
        q_0 = (dcm[2,1] - dcm[1,2])/(4*q_1)
        q_2 = (dcm[0,1] + dcm[1,0])/(4*q_1)
        q_3 = (dcm[2,0] + dcm[0,2])/(4*q_1)
    elif max(q_sq) == q_2_sq:
        q_2 = np.sqrt(q_2_sq)
        q_0 = (dcm[0,2] - dcm[2,0])/(4*q_2)
        q_1 = (dcm[0,1] + dcm[1,0])/(4*q_2)
        q_3 = (dcm[1,2] + dcm[2,1])/(4*q_2)
    elif max(q_sq) == q_3_sq:
        q_3 = np.sqrt(q_3_sq)
        q_0 = (dcm[1,0] - dcm[0,1])/(4*q_3)
        q_1 = (dcm[2,0] + dcm[0,2])/(4*q_3)
        q_2 = (dcm[1,2] + dcm[2,1])/(4*q_3)

    # put quaternion components into array
    q = np.array([q_0, q_1, q_2, q_3])

    # choose shortest rotation path (q0 > 0)
    if np.sign(q[0]) < 0:
        q = -1*q

    return q

# Define function to calculate rotation matrix given input and output
# a is input vector, b is output vector (a is rotated to b)
# Source: https://math.stackexchange.com/questions/180418/calculate-rotation-matrix-to-align-vector-a-to-vector-b-in-3d
def calc_rotation(a,b):
        v = np.cross(a,b)
        c = np.dot(a,b)
        R = np.identity(3) + Skew(v) + np.matmul(Skew(v),Skew(v))*1/(1+c)
        return R

# Define target calculation function
def target_calc(r_ECI):
    x_ECI = np.array([1,0,0])   # x axis vector in ECI frame
    target_vec_x = -1*r_ECI
    R = calc_rotation(x_ECI,target_vec_x)
    q = dcm_to_euler(R)
    return q

#q = target_calc(np.array([1/np.sqrt(2),1/np.sqrt(2),0]))
#print(q)

