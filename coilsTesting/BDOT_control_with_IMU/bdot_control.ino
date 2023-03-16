/**@file bdot_control.ino
 * 
 * @brief Implementation of the BDOT algorithm.
 * 
 * This file was transcribed from the python version on github.
 * The original code is left in a comment at the end of this file.
 */
#include "bdot_control.h"

//the constant that converts the cross product to amps
const long int current_constant = 67200;


void bdot_control(double coils_current[], double mf[], double av[]) {
  //coils_current is the cross product of the magnetic_field array and
  //the angular velocity array multiplied by the current constant
  coils_current[0] = current_constant * (mf[1]*av[2] - mf[2]*av[1]);
  coils_current[1] = current_constant * (mf[2]*av[0] - mf[0]*av[2]);
  coils_current[2] = current_constant * (mf[0]*av[1] - mf[1]*av[0]);

  //if the output command has more current than we can produce, scale it to the max (0.158)
  if (abs(coils_current[0]) + abs(coils_current[1]) + abs(coils_current[1]) > 0.158) {
    double coils_current_norm = 
      sqrt(
        sq(coils_current[0]) + 
        sq(coils_current[1]) + 
        sq(coils_current[2])
      );
    
    coils_current[0] = 0.158 * coils_current[0] / coils_current_norm;
    coils_current[1] = 0.158 * coils_current[1] / coils_current_norm;
    coils_current[2] = 0.158 * coils_current[2] / coils_current_norm;
  }

  return;
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
