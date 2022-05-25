# Target calculation test and visualization
import numpy as np
import matplotlib.pyplot as plt
from target_calc_DCM import *

# input R_ECI
R_ECI = np.array([0,1/np.sqrt(2),1/np.sqrt(2)])

# ECI x-axis vector
x_ECI = np.array([1,0,0])

# Obtain output rotation matrix
rot_matrix = target_calc(R_ECI)

# Use rotation matrix to compute target vector
R_target = np.dot(rot_matrix, x_ECI)
print(R_target)

# Make an Earth
R = 1

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, projection='3d')

u = np.linspace(0, 2*np.pi, 100)
v = np.linspace(0, np.pi, 100)

X = np.outer(np.cos(u), np.sin(v))
Y = np.outer(np.sin(u), np.sin(v))
Z = np.outer(np.ones(np.size(u)), np.cos(v))
X = (X)*R
Y = (Y)*R
Z = (Z)*R
ax.plot_surface(X,Y,Z, rstride=4, cstride=4, color='b', alpha=0.2)

# Add ECI and target vectors to plot
ax.quiver(0,0,0,R_ECI[0],R_ECI[1],R_ECI[2],length=1,arrow_length_ratio = 0.03,color='red',linewidth=2,label='Position Vector in ECI Frame')
ax.quiver(0,0,0,x_ECI[0],x_ECI[1],x_ECI[2],length=1,arrow_length_ratio=0.03,color='purple',linewidth=2,label='X-Axis in ECI Frame')
ax.quiver(0,0,0,R_target[0],R_target[1],R_target[2],length=1,arrow_length_ratio=0.03,color='green',linewidth=2,label='X-Axis in Target Frame')
ax.set_xlabel('X ECI')
ax.set_ylabel('Y ECI')
ax.set_zlabel('Z ECI')

ax.set_title('Target Calculation (Camera aligned with X-axis)')
fig.legend()
fig.show()

# Keep figures open
input()