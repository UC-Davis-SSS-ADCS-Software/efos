import numpy as np
from ADCS_Constants import R_SENSOR_TO_BODY
from mag_processing import mag_processing
import matplotlib.pyplot as plt

# test cases
delta_t = 0.200
x_raw = []
y_raw = []
z_raw = []
x_proc = []
y_proc = []
z_proc = []
for i in range(0,20):
    m_current = np.array([np.cos(0.1 * i * np.pi),
                          np.sin(0.2 * i * np.pi),
                          0.05 * i])
    if i == 0:
        m_prev = np.dot(R_SENSOR_TO_BODY, m_current)

    print("UNFILTERED READING:")
    print(m_current)
    x_raw.append(m_current[0])
    y_raw.append(m_current[1])
    z_raw.append(m_current[2])
    m_filtered = mag_processing(m_current[0], m_current[1], m_current[2], m_prev[0], m_prev[1], m_prev[2], delta_t)
    print("FILTERED READING:")
    print(m_filtered)
    m_prev = m_filtered
    x_proc.append(m_filtered[0])
    y_proc.append(m_filtered[1])
    z_proc.append(m_filtered[2])
    print("-----------------")
plt.figure(figsize=(10,10))
plt.plot(x_raw, label="x_raw", linestyle='--', color='r')
plt.plot(x_proc, label="x_proc", linestyle='-', color='r')
plt.plot(y_raw, label="y_raw", linestyle='--', color='b')
plt.plot(y_proc, label="y_proc", linestyle='-', color='b')
plt.plot(z_raw, label="z_raw", linestyle='--', color='g')
plt.plot(z_proc, label="z_proc", linestyle='-', color='g')
plt.legend()
plt.show()


