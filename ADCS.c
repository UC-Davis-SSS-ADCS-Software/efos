/**@file ADCS.c
 *
 * @brief Implementation of Intellisat interface to the ADCS software.
 *
 * @author Jacob Tkeio (jacobtkeio@gmail.com)
 * @date 8/5/2023
 */

#include "ADCS.h"
#include "sofa/20210512/c/src/sofa.h"


void ADCS_MAIN(
	adcs_mode mode,
	int year,
	int month,
	int day,
	int hour,
	int min,
	double sec
) {
	iauDtf2d(
		"UTC",
		year,
		month,
		day,
		hour,
		min,
		(double) sec,
		&UTC1,
		&UTC2
	);

}





