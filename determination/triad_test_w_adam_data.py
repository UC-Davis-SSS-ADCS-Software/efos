# Test of Triad script with Adams
import numpy as np
import pandas as pd
import triad_class_DCM

# read data from excel file into numpy array
data = pd.read_excel('C:/Users/Graham Bough/Documents/SSS Club/Current Determination Software/TRIAD test data.xlsx')
data_np = np.array(data)

# create arrays for inputs to Triad
sun_ECI = np.array([data_np[:,0],data_np[:,1],data_np[:,2]])
sun_meas = np.array([data_np[:,3],data_np[:,4],data_np[:,5]])
mag_ECI = np.array([data_np[:,6],data_np[:,7],data_np[:,8]])
mag_meas = np.array([data_np[:,9],data_np[:,10],data_np[:,11]])

# create arrays for DCM outputs from data
DCM_data = np.array([data_np[:,12],data_np[:,13],data_np[:,14],data_np[:,15],data_np[:,16],data_np[:,17],data_np[:,18],data_np[:,19],data_np[:,20]])

# loop through data and calculate DCM components
DCM_array = np.empty((9,len(data_np[:,0])))
for i in range(len(data_np[:,0])):
    triad_object = triad_class_DCM.TRIAD(sun_meas[:,i], mag_meas[:,i], sun_ECI[:,i], mag_ECI[:,i])
    DCM_triad = triad_object.triad()
    DCM_array[:,i] = DCM_triad.flatten()

# compare DCM data to computed DCM elements
error = np.abs(DCM_data-DCM_array)
print(np.amax(error))