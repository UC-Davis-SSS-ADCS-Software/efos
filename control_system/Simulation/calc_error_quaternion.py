# Calculate error between measured and target quaternion
import numpy as np

# Function definitions to calculate vector and scalar quaternion errors
# q is measured quaternion and qc is target quaternion
def calc_quat_vector_error(q,qc):
    delta_q_vec = np.array([
        q[1]*qc[0] + q[2]*qc[3] - q[3]*qc[2] - q[0]*qc[1],
        -q[1]*qc[3] + q[2]*qc[0] + q[3]*qc[1] - q[0]*qc[2],
        q[1]*qc[2] - q[2]*qc[1] + q[3]*qc[0] - q[0]*qc[3]
    ])
    return delta_q_vec

def calc_quat_scalar_error(q,qc):
    delta_q_scal = q[1]*qc[1] + q[2]*qc[2] + q[3]*qc[3] + q[0]*qc[0]
    return delta_q_scal