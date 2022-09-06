## PD Attitude Controller
import numpy as np
import math
import calc_error_quaternion

# Define function to multiply quaternions
# (https://stackoverflow.com/questions/39000758/how-to-multiply-two-quaternions-by-python-or-numpy)
def quat_multiply(Q1, Q2):
    q0, q1, q2, q3 = Q1
    p0, p1, p2, p3 = Q2
    return np.array([-p1*q1 - p2*q2 - p3*q3 + p0*q0,
                    p1*q0 + p2*q3 - p3*q2 + p0*q1,
                    -p1*q3 + p2*q0 + p3*q1 + p0*q2,
                    p1*q2 - p2*q1 + p3*q0 + p0*q3])


def Skew(v):
    S = np.array([
        [0, -1*v[2], v[1]],
        [v[2], 0, -1*v[0]],
        [-1*v[1], v[0], 0]
    ],dtype=object)
    return S


def quat_error(Q1, Q2):
    q0, q1, q2, q3 = Q1
    p0, p1, p2, p3 = Q2
    delta_q0 = q0*p0+q1*p1+q2*p2+q3*p3
    Theta_q_0 = q0*np.identity(3)-Skew(np.array([q1,q2,q3]))
    Theta_q = np.append(-np.array([[q1,q2,q3]]),[Theta_q_0[0,:]], axis=0)
    Theta_q = np.append(Theta_q,[Theta_q_0[1,:]], axis=0)
    Theta_q = np.append(Theta_q,[Theta_q_0[2,:]], axis=0)
    delta_q123 = np.dot(np.transpose(Theta_q),np.array([p0,p1,p2,p3]))
    return np.array([delta_q0,delta_q123[0],delta_q123[1],delta_q123[2]])


def vector_magnitude(vector):
    return np.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

class Attitude_Control:

    def __init__(self, target_attitude, measured_attitude, target_ang_rate, measured_ang_rate):
        self.target_attitude = target_attitude
        self.measured_attitude = measured_attitude
        self.target_ang_rate = target_ang_rate
        self.measured_ang_rate = measured_ang_rate

    # Calculate attitude error quaternion
    def attitude_error(self):
        attitude_error = quat_error(self.target_attitude, self.measured_attitude)
        #target_attitude_conj = np.array([self.target_attitude[0], -1*self.target_attitude[1], -1*self.target_attitude[2], -1*self.target_attitude[3]])
        #attitude_error = quat_multiply(target_attitude_conj, self.measured_attitude)
        #attitude_vector_error = calc_error_quaternion.calc_quat_vector_error(self.measured_attitude,self.target_attitude)
        #attitude_scalar_error = calc_error_quaternion.calc_quat_scalar_error(self.measured_attitude,self.target_attitude)
        #attitude_error = np.array([attitude_scalar_error,attitude_vector_error[0],attitude_vector_error[1],attitude_vector_error[2]])
        return attitude_error

    # Calculate angular rate error
    def ang_rate_error(self):
        ang_rate_error = vector_magnitude(self.target_ang_rate) - vector_magnitude(self.measured_ang_rate)
        return ang_rate_error

    # PD Controller
    def attitude_control(self):
        #Kp = 100*np.array([0.01840966, 0.01754317, 0.00950984])  # Proportional Gain
        #Kd = 100*np.array([0.01522466, 0.01450809, 0.00786457])   # Derivative Gain
        Kp = 0.1
        Kd = 0.5
        attitude_error = self.attitude_error()  # Calculate attitude error
        #print(-1*Kp*attitude_error[1:4])
        #print(self.measured_ang_rate[0])
        #ang_rate_error = self.ang_rate_error()  # Calculate angular rate error
        control_torque = -1*np.multiply(Kp,attitude_error[1:4]) - np.multiply(Kd,self.measured_ang_rate)   # Calculate control torque
        max_speed = 8000*0.10472 # rad/s, max reaction wheel speed
        if self.measured_ang_rate[2] > max_speed:
            control_torque[2] = 0
        #if control_torque[2] > 0.1e-3:
            #control_torque[2] = 0.1e-3
        #control_torque = -1*Kp*attitude_error[1:4] - Kd*self.measured_ang_rate
        #print("Proportional Term",Kp*attitude_error[1:4])
        #print("Derivative Term", Kd*self.measured_ang_rate)
        return control_torque
