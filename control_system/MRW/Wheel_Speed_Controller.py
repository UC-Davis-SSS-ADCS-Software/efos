# Wheel_Speed_Controller outputs an MRW speed command using controller torque.
# Inputs: des_torque (from RW controller) (N * m)
#         rw_angvel (current RW speed) (rad/s)
#         loop_period (elapsed time) (s)
# Outputs: command_vector (new MRW speed) (rad/s)


from ADCS_Constants import MAX_RW_ANGVEL, RW_MOI

def wheelSpeedController(des_torque, rw_angvel, loop_period):

    # calculate new wheel speed
    command_vector = rw_angvel + (des_torque * loop_period / RW_MOI)
    if (command_vector > MAX_RW_ANGVEL):
        command_vector = MAX_RW_ANGVEL
    elif (command_vector < MAX_RW_ANGVEL * -1):
        command_vector = -1 * MAX_RW_ANGVEL
    return command_vector