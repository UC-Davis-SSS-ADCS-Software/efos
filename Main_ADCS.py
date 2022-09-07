from ADCS_Constants import *
from determination.calendar_date_to_JD import calendar_date_to_JD
from determination.SensorProcessing import mag_processing, imu_processing
from determination.eclipseCheck import eclipseCheck
from determination.sunLookup import sunLookup
from determination.IGRF.igrf_mag_vector_ecef import igrf_mag_vector_ecef
from determination.TRIAD import triad_class
from determination.ECI_TO_ECEF import ECI_TO_ECEF
from SGP4_orbit_propagator.TLE_to_pos_vel import TLE_to_pos_vel as sgp4
from bdot_control.code_for_hardware_testing import bdot_control
from control_system import Attitude_Controller
from control_system.MRW.Wheel_Speed_Controller import wheelSpeedController
from control_system.rotisserie import rotisserie

def Main_ADCS(sunsensor_inputs, mag_inputs, angvel_inputs, datetime, mode, TLE1, TLE2, w_rw, delta_t):

    # Apply filters and offsets to sensor inputs
    mag_field_body = mag_processing(mag_inputs)
    body_angvel = imu_processing(angvel_inputs)

    # Define date in all formats (mostly for debug purposes -- eventually we should switch to a consistent date format)
    # This assumes we receive the date and time as a Python datetime object
    # TODO check with CS which format they'll input to the function
    date_as_array = [datetime.year, datetime.month, datetime.day, datetime.hour, datetime.minute, datetime.second]
    epoch_time = calendar_date_to_JD(date_as_array)

    # Ensure mode is consistent format
    mode = str(mode).upper()

    # If detumbling, only use magnetorquers (no HDD or MRW)
    if mode == 'DETUMBLE':
        mrw_gain = [0, 0, 0]
        hdd_gain = [0, 0, 0]
        bdot_gain = BDOT_GAIN

    # If MRW mode, only use MRW (no HDD or BDOT)
    elif mode == 'MRW POINTING' or mode == 'MRW IMAGING': # only MRW
        mrw_gain = [PROP_CONTROL_MRW, INTEGRAL_CONTROL_MRW, DERIVATIVE_CONTROL_MRW]
        hdd_gain = [0, 0, 0]
        bdot_gain = 0

    # If HDD mode, only use HDD (no MRW or BDOT)
    elif mode == 'HDD POINTING' or mode == 'HDD IMAGING': # only HDD
        mrw_gain = [0, 0, 0]
        hdd_gain = [PROP_CONTROL_HDD, INTEGRAL_CONTROL_HDD, DERIVATIVE_CONTROL_HDD]
        bdot_gain = 0

    # If mode command is invalid, return an error
    else:
        return -1 # TODO check in with CS re: error codes

    if mode == 'DETUMBLE':
        # detumble if IMU is above threshold
        # TODO does CS check for this or should we?
        if abs(body_angvel[0]) > IMU_THRESH[0] or abs(body_angvel[1]) > IMU_THRESH[1] or abs(IMU_THRESH[2]) > IMU_THRESH[2]:
            dipole = bdot_control(mag_field_body, BDOT_GAIN)
            return dipole
        else:
            return [0, 0, 0]

    # MAIN ADCS LOOP
    # If REALOP is already detumbled, check if in eclipse before attempting to calculate attitude
    elif eclipseCheck(sunsensor_inputs, ECLIPSE_THRESHOLD) == False:

        # SUN PROCESSING
        # TODO convert sun sensors testing code to sun processing function
        sun_pos_body = sun_processing(sunsensor_inputs)

        try:
            # Calculate rotation matrices
            R_eci2ecef = ECI_TO_ECEF(date_as_array)
            R_ecef2eci = np.linalg.inv(R_eci2ecef)

            # Calculate orbit position using TLE
            [pos_eci, vel_eci] = sgp4(TLE1, TLE2, epoch_time)
            pos_ecef = np.dot(R_eci2ecef, pos_eci)

            # Get reference vectors using sun lookup and IGRF
            sun_pos_eci = sunLookup(datetime)
            mag_vector_ecef = igrf_mag_vector_ecef(pos_ecef, datetime)
            mag_field_eci = np.dot(R_ecef2eci, mag_vector_ecef)

            # Calculate attitude using TRIAD
            triad_object = triad_class.TRIAD(sun_pos_body, mag_field_body, sun_pos_eci, mag_field_eci)
            q_measured = triad_object.triad()
            # TODO: figure out how to use target calculation
            [q_desired, w_desired] = Target_calculation(mode,pos_eci,vel_eci)
            w_measured = body_angvel[2] # angular velocity of body about z-axis
            controller_object = Attitude_Controller.Attitude_Control(q_desired, q_measured, w_desired, w_measured)
            des_torque = controller_object.attitude_control()
            command_vector = wheelSpeedController(des_torque, w_rw, delta_t) # TODO: get loop period or elapsed time per function call
        except:
            # Enter rotisserie mode if ADCS fails
            w_body = body_angvel[2] # angular velocity of body about z-axis
            command_vector = rotisserie(J_CS, w_body, RW_MOI, w_rw)
        return command_vector






