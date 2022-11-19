import numpy as np

def R_Sensor_to_Body(theta): 
    theta = np.radians(theta)
    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c, -s, 0), (s, c, 0), (0, 0, 1)))
    print("\n\n\n Rotation Matrix:")
    print(R) 
    return(R)

