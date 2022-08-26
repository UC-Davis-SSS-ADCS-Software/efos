import sys
sys.path.append("..")

import numpy as np
import triad_class
import random

# Define function to multiply quaternions
# (https://stackoverflow.com/questions/39000758/how-to-multiply-two-quaternions-by-python-or-numpy)
def quat_multiply(Q1, Q2):
    q0, q1, q2, q3 = Q1
    p0, p1, p2, p3 = Q2
    return np.array([-p1*q1 - p2*q2 - p3*q3 + p0*q0,
                    p1*q0 + p2*q3 - p3*q2 + p0*q1,
                    -p1*q3 + p2*q0 + p3*q1 + p0*q2,
                    p1*q2 - p2*q1 + p3*q0 + p0*q3])

# Initialize random number generator
random.seed()

# Direction Cosine Matrix error terms
e1 = random.uniform(0, 0.1)
e2 = random.uniform(0, 0.1)
e3 = random.uniform(0, 0.1)
e4 = random.uniform(0, 0.1)
e5 = random.uniform(0, 0.1)
e6 = random.uniform(0, 0.1)

# TRIAD test function
def test_triad(r, p, y):

    # Euler Angle input
    r = np.radians(r)
    p = np.radians(p)
    y = np.radians(y)

    # Convert inputted Euler Angles to a Quaternion
    q0 = np.cos(r/2)*np.cos(p/2)*np.cos(y/2)+np.sin(r/2)*np.sin(p/2)*np.sin(y/2)
    q1 = np.sin(r/2)*np.cos(p/2)*np.cos(y/2)-np.cos(r/2)*np.sin(p/2)*np.sin(y/2)
    q2 = np.cos(r/2)*np.sin(p/2)*np.cos(y/2)+np.sin(r/2)*np.cos(p/2)*np.sin(y/2)
    q3 = np.cos(r/2)*np.cos(p/2)*np.sin(y/2)-np.sin(r/2)*np.sin(p/2)*np.cos(y/2)

    q = np.array([q0, q1, q2, q3])

    # Display Quaternion
    print("Quaternion:")
    print(q)

    # Print Quaternion magnitude (should be very close to 1)
    s = np.sqrt(q0*q0 + q1*q1 + q2*q2 + q3*q3)
    print(s)

    # Define measured and reference vectors intitially pointing in same direction
    acc_meas = np.array([0.0, 0.0, -1.0])
    mag_meas = np.array([1.0, 0.0, 0.0])
    acc_ref = np.array([0.0, 0.0, -1.0]) # constant reference vector
    mag_ref = np.array([1.0, 0.0, 0.0]) # constant reference vector

    # Convert Quaternion to Direction Cosine Matrix
    rot = np.array([
        [1-2*(q2*q2+q3*q3), 2*(q1*q2-q3*q0), 2*(q1*q3+q2*q0)],
        [2*(q1*q2+q3*q0), 1-2*(q1*q1+q3*q3), 2*(q2*q3-q1*q0)],
        [2*(q1*q3-q2*q0), 2*(q2*q3+q1*q0), 1-2*(q1*q1+q2*q2)]
    ])

    # Display Direction Cosine Matrix
    print("Direction Cosine Matrix:")
    print(rot)
    print()

    # Display Determinant of DCM
    print("Determinant of DCM:")    # proper matrix is det(rot)=1, improper if det(rot)=-1
    print(np.linalg.det(rot))
    print()

    # Rotate measured vectors using DCM and add error terms
    acc_meas_rot = np.dot(rot, acc_meas)
    acc_meas_rot = np.array([acc_meas_rot[0] + e1, acc_meas_rot[1] + e2, acc_meas_rot[2] + e3])
    acc_meas_rot = acc_meas_rot / np.linalg.norm(acc_meas_rot)
    mag_meas_rot = np.dot(rot, mag_meas)
    mag_meas_rot = np.array([mag_meas_rot[0] + e4, mag_meas_rot[1] + e5, mag_meas_rot[2] + e6])
    mag_meas_rot = mag_meas_rot / np.linalg.norm(mag_meas_rot)

    # Display rotated measured vectors
    print("Output Rotated Measurement Vectors:")
    print("Acc:", acc_meas_rot)
    print("Mag:", mag_meas_rot)
    print()

    # Create TRIAD object using measured and reference vectors
    triad_object = triad_class.TRIAD(acc_meas_rot, mag_meas_rot, acc_ref, mag_ref)

    # Use triad() function to calculate quaternion from inputted vectors
    rot_triad = triad_object.triad()
    print("Unmodified Output:", rot_triad)
    print()

    # Create array for known quaternion to compare with calculated quaternion
    rot_input = np.array([q0, q1, q2, q3])

    # Make sure that sign is correct, if not multipy q by -1 (Note: -q represents same rotation as +q)
    if (np.sign(rot_triad[0]) != np.sign(rot_input[0])):
        rot_triad = np.dot(-1, rot_triad)

    # Calculate conjugate of input quaternion
    rot_input_conj = np.array([rot_input[0], -1*rot_input[1], -1*rot_input[2], -1*rot_input[3]])
    print("Rotation input conjugate: ", rot_input_conj)

    # Calculate quaternion that represents rotation between input and output
    error_quat = quat_multiply(rot_input_conj, rot_triad)
    print("Error quaternion: ", error_quat)

    # Find angle of rotation between input and output
    error_angle = 2*np.arctan2(np.linalg.norm(error_quat[1:3]), error_quat[0])

    print("Angle between input and output: ", np.degrees(error_angle))
    print()

    # Display test results
    print("Output Rotations:")
    print("Input:", rot_input)
    print("Output:", rot_triad)

    return np.degrees(error_angle)

# Format array printing
if __name__ == "__main__":
    # https://stackoverflow.com/questions/22222818/how-to-printing-numpy-array-with-3-decimal-places
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    test_triad(-10, 20, 30)