/**@file ADCS.h
 *
 * @brief Intellisat interface to ADCS software.
 *
 * @author Jacob Tkeio (jacobtkeio@gmail.com)
 *
 * @date 7/30/2023
 */

#ifndef ADCS_H
#define ADCS_H

#include "adcs_math/matrix.h"


//Intellisat functions required in ADCS_MAIN
//...



//State variables
mat3 realop_attitude;
double julian_date;


typedef enum {
	DETUMBLE,
	HDD,
	MRW
} adcs_mode;


void ADCS_MAIN(adcs_mode, double julian_date);

double calculate_julian_date(
	int year,
	int month,
	int day,
	int hour,
	int min,
	int sec
);



#endif//ADCS_H





