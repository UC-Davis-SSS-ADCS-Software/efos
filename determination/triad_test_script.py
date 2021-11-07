import sys
sys.path.append("..")

import numpy as np
import triad_class

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

    # Rotate measured vectors using DCM
    acc_meas_rot = np.dot(rot, acc_meas)
    mag_meas_rot = np.dot(rot, mag_meas)

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

    # Check if known quaternion matches calculated quaternion
    valid = np.allclose(rot_triad, rot_input)

    # If quaternions do match check negative calculated quaternion (Note: -q represents same rotation as +q)
    if (valid == False):
        rot_triad = np.dot(-1, rot_triad)
        valid = np.allclose(rot_triad, rot_input)

    # Display test results
    print("Output Rotations:")
    print("Input:", rot_input)
    print("Output:", rot_triad)
    print("Valid:", valid)

    return valid

# Format array printing
if __name__ == "__main__":
    # https://stackoverflow.com/questions/22222818/how-to-printing-numpy-array-with-3-decimal-places
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    test_triad(150, 0.9, 34)