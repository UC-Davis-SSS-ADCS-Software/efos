/**@file HDD_CONST_TEST.c
 *
 * @brief Tests HDD wheel speed at three different times
 * 		after setting up constant control input.
 */
//#include "SSS_MCU.h"


/**@brief Test HDD speed from rest over time at a constant input.
 *
 * @param run_time The length of the test.
 * @param input The power and direction sent to the HDD (-100 to 100).
 *
 * @return Void.
 */
void HDD_CONST_TEST(double run_time, int input) {
/*
During the run time, print timestamp and wheel speed info, presumably so
that wheel speed vs time can be graphed in excel or a similar program.
After, make sure the wheel stops!

Indeed, we cannot write test code until we have some CS interface ("SSS_MCU.h")
to the hardware. We'd need HDD control, HDD rotation data, and time access.

We should also think about how to run the test after uploading it.
Maybe a flat delay after a button press?
*/
}
