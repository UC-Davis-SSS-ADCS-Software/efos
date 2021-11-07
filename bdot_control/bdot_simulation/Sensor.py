import numpy as np
import random
import globals

# Sensor Update Rate
globals.nextSensorUpdate = 1

# Sensor function
def Sensor(BB, pqr):

    # Initialize random number generator
    random.seed()

    # Bias and Noise
    MagscaleBias = 4e-7 # Teslas
    MagFieldBias = MagscaleBias*random.uniform(-1,1)

    MagscaleNoise = 1e-5 # Teslas
    MagFieldNoise = MagscaleNoise*random.uniform(-1, 1)

    AngscaleBias = 0.01 # rad/s
    AngFieldBias = AngscaleBias*random.uniform(-1, 1)

    AngscaleNoise = 0.001 # rad/s
    AngFieldNoise = AngscaleNoise*random.uniform(-1, 1)

    for i in range(3):
        BB[i] = BB[i] + MagFieldBias + MagFieldNoise
        pqr[i] = pqr[i] + AngFieldBias + AngFieldNoise
    
    return np.array([BB, pqr])