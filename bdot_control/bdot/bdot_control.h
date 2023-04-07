/**@file bdot_control.h
 * 
 * @brief The interface to the BDOT algorithm.
 * 
 * This function will break inexplicably if passed
 *  any arrays less than length 3.
 */
#ifndef BDOT_CONTROL
#define BDOT_CONTROL

/**@brief Calculate a dipole command for all three coils given our
 *  magnetic field and angular velocity data.
 * 
 * @param coils_current An array to be pre-allocated that will contain
 *      the output after bdot_control runs.
 *    Format: [X, Y, Z] Amperes
 * @param mf The magnetic field vector.
 *    Format: [X, Y, Z] Micro Teslas
 * @param av The angular velocity vector.
 *    Format: [X, Y, Z] Radians per Second
 * 
 * @return Void.
 */
void bdot_control(double coils_current[], double mf[], double av[]);

#endif//BDOT_CONTROL
