/**@file quaternion.c
 *
 * @brief Implementation of quaternion utility functions.
 *
 * Note that REALOP-1's MCU works best with floats, not doubles.
 * 	Especially note that all <math.h> functions have
 * 	a float-specific version you must use!
 *
 * These functions were designed with the idea in mind that
 * 	a quaternion could be passed as both an input and the output
 * 	without issue, even if some pass-by-value arguments are later
 * 	converted to pass-by-reference.
 *
 * Many of these functions use their pass-by-value arguments to
 * 	store temporary variables. Not great form, but cost effective!
 *
 * @author Jacob Tkeio (jacobtkeio@gmail.com) 6/3/2023
 */

#include <math.h>
#include "quaternion.h"
#include "vector.h"


void quat_set(float scalar, vec3 vector, quat *output) {
	(*output).scalar = scalar;
	(*output).vector = vector;
}


void quat_scalar(float scalar, quat quaternion, quat *output) {
	vec_scalar(scalar, quaternion.vector, &(quaternion.vector));

	quat_set(
		scalar * quaternion.scalar,
		quaternion.vector,
		output
	);
}


void quat_mult(quat left, quat right, quat *output) {
	vec3 new_vector;
	float new_scalar =
		left.scalar * right.scalar -
		vec_dot(left.vector, right.vector);

	vec3 ab;
	vec3 ba;
	vec3 axb;

	vec_scalar(left.scalar, right.vector, &ab);
	vec_scalar(right.scalar, left.vector, &ba);
	vec_cross(left.vector, right.vector, &axb);

	vec_add(ab, ba, &new_vector);
	vec_add(new_vector, axb, &new_vector);

	quat_set(
		new_scalar,
		new_vector,
		output
	);
}


void quat_norm(quat quaternion, quat *output) {
	quat_scalar(
		1 / quat_mag(quaternion),
		quaternion,
		output	
	);
}


void quat_conj(quat quaternion, quat *output) {
	vec_scalar(-1.0f, quaternion.vector, &(quaternion.vector));
	quat_set(
		quaternion.scalar,
		quaternion.vector,
		output
	);
}


void quat_inverse(quat quaternion, quat *output) {
	quat_conj(quaternion, &quaternion);
	quat_norm(quaternion, output);
}


void quat_from(float angle, vec3 vector, quat *output) {
	vec_norm(vector, &vector);
	vec_scalar(
		sinf(angle * 0.5f),
		vector,
		&vector
	);

	quat_set(
		cosf(angle * 0.5f),
		vector,
		output
	); 
} //quat. U = (cos a/2, n*sin a/2) where a is an angle and n is a unit vector


void quat_rotate_vec(vec3 vector, quat quaternion, vec3 *output) {
	quat vector_wrapper = {0.0f, vector};

	quat_mult(quaternion, vector_wrapper, &vector_wrapper);
	quat_conj(quaternion, &quaternion);
	quat_mult(vector_wrapper, quaternion, &vector_wrapper);

	(*output) = vector_wrapper.vector;
}


float quat_mag(quat quaternion) {
	return sqrtf(
		quaternion.scalar * quaternion.scalar +
		vec_dot(quaternion.vector, quaternion.vector)
	);
}
