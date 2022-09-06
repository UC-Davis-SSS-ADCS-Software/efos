# ADCS Flight Operating Software

## Modules Used
- numpy
- pyIGRF
- math
- sgp4

## Features
### Eclipse Check 
- <b>[Link](determination/eclipseCheck.py)</b>
- <b>Status:</b> code completed, need constant threshold values from sun sensors before hardware testing

### Sun Sensor Processing
- <b>[Link](Sun_Sensors/Sun_Sensors_Testing_Code_V0.py)</b>
- <b>Status:</b> in progress with sun sensor calibration; will need to be reformatted for flight

### Magnetometer Processing
- <b>[Link](determination/SensorProcessing/mag_processing.py)</b>
- <b>Status:</b> code completed, need hardware testing to finalize low-pass filter parameters. Also need to calculate rotation matrix from sensor frame to body frame

### IMU Processing
- <b>[Link](determination/SensorProcessing/mag_processing.py)</b>
- <b>Status:</b> code completed, need hardware testing to finalize low-pass filter parameters. Also need to calculate rotation matrix from sensor frame to body frame

### Orbit Propagator (SGP4)
- <b>[Link](SGP4_orbit_propagator/TLE_to_pos_vel.py)</b>
- <b>Status:</b> code completed, need to verify with alternative SGP4 package (i.e. MATLAB or Java)

### Sun Model
- <b>[Link](determination/sunLookup.py)</b>
- <b>Status:</b> code completed and tested against a few MATLAB cases, but could use further testing

### Magnetic Field Model (IGRF)
- <b>[Link](determination/IGRF/igrf_mag_vector_ecef.py)</b>
- <b>Status:</b> completed and verified!

### Attitude Determination (TRIAD)
- <b>[Link](determination/TRIAD/triad_class.py)</b>
- <b>[Example Usage](determination/triad_test_script.py)</b>
- <b>Status:</b> completed and verified!

### BDot Controller for Detumbling
- <b>[Link](bdot_control/code_for_hardware_testing/bdot_control.py)</b>
- <b>Status:</b> code completed, waiting on hardware testing

### Attitude Target Calculation
- <b>[Link](determination/TargetCalculation/target_calc.py)</b>
- <b>[Example Usage](determination/target_calc_test.py)</b>
- <b>Status:</b> completed and verified!

### Reaction Wheel Controller
- <b>[Link](control_system/Attitude_Controller.py)</b>
- <b>Status:</b> n/a, need to check

### Wheel Speed Controller
- <b>[Link](control_system/MRW/MRW_Test.py)</b>
- <b>Status:</b> need hardware testing for tuning, then restructuring code for flight
