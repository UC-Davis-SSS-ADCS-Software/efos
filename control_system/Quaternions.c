// define functions for quaternion operations
// used primarily for TRIAD, attitude controller (RW controller), and target calc

#include <stdio.h>
#include <math.h>

// multiply 2 quaternions
// quat1 and quat2 are multiplied
// quat3 stores output
void quat_multiply(float quat1[4], float quat2[4], float quat3[4]) {
   
    // get individual quaternion components
    float q0 = quat1[0];
    float q1 = quat1[1];
    float q2 = quat1[2];
    float q3 = quat1[3];
    float p0 = quat2[0];
    float p1 = quat2[1];
    float p2 = quat2[2];
    float p3 = quat2[3];

    // multiply components
    quat3[0] = -p1*q1 - p2*q2 - p3*q3 + p0*q0;
    quat3[1] = p1*q0 + p2*q3 - p3*q2 + p0*q1;
    quat3[2] = -p1*q3 + p2*q0 + p3*q1 + p0*q2;
    quat3[3] = p1*q2 - p2*q1 + p3*q0 + p0*q3;

}

int main() {
    float quat1[4];
    float quat2[4];
    float quat3[4];
    
    quat1[0] = 2.0;
    quat1[1] = 1.0;
    quat1[2] = -4.0;
    quat1[3] = -5.0;

    quat2[0] = 4.0;
    quat2[1] = -0.5;
    quat2[2] = 7.0;
    quat2[3] = 3.0;
    
    quat_multiply(quat1, quat2, quat3);

    printf("%f", quat3[0]);
    printf("%f", quat3[1]);
    printf("%f", quat3[2]);
    printf("%f", quat3[3]);
    return 0;
}