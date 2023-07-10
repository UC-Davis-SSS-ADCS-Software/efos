/**@file bdot_control.c
 * 
 * @brief Implementation of the BDOT algorithm.
 * 
 * This file was transcribed from the python version on github.
 * The original code is left in a comment at the end of this file.
 *
 * @author Jacob Tkeio (jacobtkeio@gmail.com) 6/11/2023
 */

#include "bdot_control.h"
#include "adcs_math/vector.h"

//the constant that converts the cross product to amps.
const float current_constant = 67200.0f;


void bdot_control(vec3 mf, vec3 av, vec3 *coils_current) {
	vec3 temp;

	vec_cross(mf, av, &temp);
	vec_scalar(current_constant, temp, &temp);

	//cap output at maximum 0.158 Amps across all coils. 
	float temp_mag = vec_mag(temp);
	if (temp_mag > 0.158f) {
		//this step is equivalent to 0.158f * normalized temp.
		vec_scalar(0.158f / temp_mag, temp, &temp);
	}

	(*coils_current) = temp;
}



/*
import numpy as np

def bdot_control(BB, pqr):
    k = 67200
    current = k*np.cross(pqr, BB)
    # current saturation if > 0.158 amps
    if np.sum(np.abs(current)) > 0.158:
        current = current/np.linalg.norm(current)*0.158
    return current
*/
