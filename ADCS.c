/**@file ADCS.c
 *
 * @brief Implementation of Intellisat interface to the ADCS software.
 *
 * @author Jacob Tkeio (jacobtkeio@gmail.com)
 * @date 8/5/2023
 */

#include "ADCS.h"


void main() {
	double jd = calculate_julian_date(
		2040,
		8,
		5,
		11,
		45,
		30
	);

	printf("%lf", jd);
}

void ADCS_MAIN(adcs_mode mode, double julian_date);

//Pay special attention to which division is integer division.
double calculate_julian_date(
	int year,
	int month,
	int day,
	int hour,
	int min,
	int sec
) {
	int adj_year;
	int adj_month;

	if (month <= 2) {
		adj_year = year-1;
		adj_month = month+12;
	} else {
		adj_year = year;
		adj_month = month;
	}

	int leap = adj_year/400 - adj_year/100 + adj_year/4;
	
	double king_julian = 365*adj_year - 679004 + leap +
		(int)(30.6001*(adj_month+1)) + day + hour/24.0 +
		min/(24.0*60.0) + sec/(24.0*60.0*60.0) + 2400000.5;

	return king_julian;
}





