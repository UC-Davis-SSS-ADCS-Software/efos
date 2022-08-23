# ADCS Flight Operating Software

## Modules Used
- numpy
- pyIGRF
- math
- sgp4

## Features
### Eclipse Check 
- <b>[Link](https://github.com/UC-Davis-SSS-ADCS-Software/efos/blob/master/flight_functions/eclipseCheck.py)</b>
- <b>Status:</b> code completed, need constant threshold values from sun sensors before hardware testing

### Sun Sensor Processing
- <b>[Link](https://github.com/UC-Davis-SSS-ADCS-Software/efos/blob/9260ca644da1fa3f2525e42952d6d7d103ab57ef/Sun_Sensors/Sun_Sensors_Testing_Code_V0.py)</b>
- <b>Status:</b> in progress with sun sensor calibration; will need to be reformatted for flight

### Magnetometer Processing
- <b>[Link](https://github.com/UC-Davis-SSS-ADCS-Software/efos/blob/master/determination/mag_processing.py)</b>
- <b>Status:</b> code completed, need hardware testing to finalize low-pass filter parameters. Also need to calculate rotation matrix from sensor frame to body frame

### IMU Processing
- <b>[Link](https://github.com/UC-Davis-SSS-ADCS-Software/efos/blob/master/determination/mag_processing.py)</b>
- <b>Status:</b> code completed, need hardware testing to finalize low-pass filter parameters. Also need to calculate rotation matrix from sensor frame to body frame

### Orbit Propagator (SGP4)
- <b>[Link](https://github.com/UC-Davis-SSS-ADCS-Software/efos/blob/master/SGP4_orbit_propagator/TLE_to_pos_vel.py)</b>
- <b>Status:</b> code completed, need to verify with alternative SGP4 package (i.e. MATLAB or Java)

### Sun Model
- <b>Link:</b> n/a (need to find)

### Magnetic Field Model (IGRF)
- <b>[Link](https://github.com/UC-Davis-SSS-ADCS-Software/efos/blob/85c08c7d222fa22567efb2a631faf74ba045fdc6/determination/igrf_mag_vector_ecef.py)</b>
- <b>Status:</b> completed and verified!

### Attitude Determination (TRIAD)
- <b>[Link](https://github.com/UC-Davis-SSS-ADCS-Software/efos/blob/85c08c7d222fa22567efb2a631faf74ba045fdc6/determination/triad_class.py)</b>
- <b>[Example Usage](https://github.com/UC-Davis-SSS-ADCS-Software/efos/blob/85c08c7d222fa22567efb2a631faf74ba045fdc6/determination/triad_test_script.py)</b>
- <b>Status:</b> completed and verified!

### BDot Controller for Detumbling
- <b>[Link](https://github.com/UC-Davis-SSS-ADCS-Software/efos/blob/85c08c7d222fa22567efb2a631faf74ba045fdc6/bdot_control/code_for_hardware_testing/bdot_control.py)</b>
- <b>Status:</b> code completed, waiting on hardware testing

### Attitude Target Calculation
- <b>[Link](https://github.com/UC-Davis-SSS-ADCS-Software/efos/blob/85c08c7d222fa22567efb2a631faf74ba045fdc6/determination/target_calc.py)</b>
- <b>[Example Usage](https://github.com/UC-Davis-SSS-ADCS-Software/efos/blob/85c08c7d222fa22567efb2a631faf74ba045fdc6/determination/target_calc_test.py)</b>
- <b>Status:</b> completed and verified!

### Reaction Wheel Controller
- <b>[Link](https://github.com/UC-Davis-SSS-ADCS-Software/efos/blob/85c08c7d222fa22567efb2a631faf74ba045fdc6/control_system/Attitude_Controller.py)</b>
- <b>Status:</b> n/a, need to check

### Wheel Speed Controller
- <b>[Link](https://github.com/UC-Davis-SSS-ADCS-Software/efos/blob/master/control_system/MRW_Test.py)</b>
- <b>Status:</b> need hardware testing for tuning, then restructuring code for flight
