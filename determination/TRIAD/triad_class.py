import numpy as np
import math

class InvalidDirectionCosineMatrix(Exception):
    pass

class TRIAD:

    def __init__(self, acc_meas, mag_meas, acc_ref, mag_ref):
        self.acc_meas = acc_meas
        self.mag_meas = mag_meas
        self.acc_ref = acc_ref
        self.mag_ref = mag_ref

    # Direction Cosine Matrix to Quaternion
    # https://www.learnopencv.com/rotation-matrix-to-euler-angles/
    def dcm_to_euler(self, dcm):
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

    # Main TRIAD function
    def triad(self):
        v_1b = np.asmatrix(self.acc_meas)    # Accelerometer vector in body frame (measurement)
        v_2b = np.asmatrix(self.mag_meas)    # Magnetic Field vector in body frame (measurement)
        v_1i = np.asmatrix(self.acc_ref)   # Accelerometer vector in reference frame
        v_2i = np.asmatrix(self.mag_ref)    # Magnetic Field vector in reference frame

        # make sure that input vectors are normalized
        if v_1b.any():
            v_1b = np.divide(v_1b, np.linalg.norm(v_1b))
        
        if v_2b.any():
            v_2b = np.divide(v_2b, np.linalg.norm(v_2b))

        if v_1i.any():
            v_1i = np.divide(v_1i, np.linalg.norm(v_1i))

        if v_2i.any():
            v_2i = np.divide(v_2i, np.linalg.norm(v_2i))

        t_1b = v_1b                     # First basis vector in body frame
        t_2b = np.cross(v_1b, v_2b)     # Second basis vector in body frame

        # TODO make sure these singularity checks actually work (works)
        if t_2b.any():
            t_2b = np.divide(t_2b, np.linalg.norm(t_2b))    # Normalize second basis vector

        t_3b = np.cross(t_1b, t_2b)     # Third basis vector in body frame

        t_1i = v_1i                     # First basis vector in reference frame
        t_2i = np.cross(v_1i, v_2i)     # Second basis vector in reference frame

        # TODO make sure these singularity checks actually work (works)
        if t_2i.any():
            t_2i = np.divide(t_2i, np.linalg.norm(t_2i))    # Normalize second basis vector

        t_3i = np.cross(t_1i, t_2i)     # Third basis vector in reference frame

        R_bt = np.concatenate((t_1b, t_2b, t_3b)).T    # Construct DCM for body frame
        R_it = np.concatenate((t_1i, t_2i, t_3i)).T    # Construct DCM for reference frame
        R_bi = np.matmul(R_bt, R_it.T)      # Construct DCM from reference frame to body frame

        return self.dcm_to_euler(R_bi)
