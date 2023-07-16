/**@file matrix.c
 *
 * @brief Implementation of 3x3 matrix utility functions.
 *
 * Note that REALOP-1's MCU works best with floats, not doubles.
 *
 * These functions were designed with the idea in mind that
 * 	a matrix could be passed as both an input and the output
 * 	without issue, even if some pass-by-value arguments are later
 * 	converted to pass-by-reference.
 *
 * @author Jacob Tkeio (jacobtkeio@gmail.com) 7/13/2023
 */

#include "matrix.h"


void mat_set(
	float x1, float x2, float x3,
	float y1, float y2, float y3,
	float z1, float z2, float z3,
	mat3 *output
) {
	(*output).x1 = x1;
	(*output).x2 = x2;
	(*output).x3 = x3;
	(*output).y1 = y1;
	(*output).y2 = y2;
	(*output).y3 = y3;
	(*output).z1 = z1;
	(*output).z2 = z2;
	(*output).z3 = z3;
}

void mat_set_from_vec(
	vec3 first,
	vec3 second,
	vec3 third,
	mat3 *output
) {
	(*output).x1 = first.x;
	(*output).x2 = second.x;
	(*output).x3 = third.x;
	(*output).y1 = first.y;
	(*output).y2 = second.y;
	(*output).y3 = third.y;
	(*output).z1 = first.z;
	(*output).z2 = second.z;
	(*output).z3 = third.z;
}

void mat_transpose(mat3 mat, mat3 *output) {
	mat_set(
		mat.x1, mat.y1, mat.z1,
		mat.x2, mat.y2, mat.z2,
		mat.x3, mat.y3, mat.z3,
		output
	);
}

void mat_scalar(float scalar, mat3 mat, mat3 *output) {
	mat_set(
		scalar * mat.x1,
		scalar * mat.x2,
		scalar * mat.x3,
		scalar * mat.y1,
		scalar * mat.y2,
		scalar * mat.y3,
		scalar * mat.z1,
		scalar * mat.z2,
		scalar * mat.z3,
		output
	);
}

void mat_mult(mat3 left, mat3 right, mat3 *output) {
	mat_set(
		left.x1*right.x1 + left.x2*right.y1 + left.x3*right.z1,
		left.x1*right.x2 + left.x2*right.y2 + left.x3*right.z2,
		left.x1*right.x3 + left.x2*right.y3 + left.x3*right.z3,
		left.y1*right.x1 + left.y2*right.y1 + left.y3*right.z1,
		left.y1*right.x2 + left.y2*right.y2 + left.y3*right.z2,
		left.y1*right.x3 + left.y2*right.y3 + left.y3*right.z3,
		left.z1*right.x1 + left.z2*right.y1 + left.z3*right.z1,
		left.z1*right.x2 + left.z2*right.y2 + left.z3*right.z2,
		left.z1*right.x3 + left.z2*right.y3 + left.z3*right.z3,
		output
	);
}

float mat_det(mat3 mat) {
	return 
		mat.x1 * (mat.y2*mat.z3 - mat.z2*mat.y3) -
		mat.x2 * (mat.y1*mat.z3 - mat.z1*mat.y3) +
		mat.x3 * (mat.y1*mat.z2 - mat.z1*mat.y2);
}





