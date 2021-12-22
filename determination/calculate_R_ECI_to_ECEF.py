
import math

# function [ R_eci2ecef ] = calc_ECI_to_ECEF( JD_i )
# Based on Seidlemann's "Explanatory Supplment to the Astronomical Almanac" page 50
# Given the JD, will return the rotation matrix to convert R_eci to R_ecef

# YOU CAN CHANGE JULIAN DATE HERE:
JD_i = 24529925.923726852

seconds_per_day = 24*3600
seconds_per_half_day = seconds_per_day/2
days_per_Julian_century = 36525
JD_epoch = 2451545.00; # JD of noon on Jan 1, 2000

JD = math.floor(JD_i)
SSN = seconds_per_day * (JD_i - JD)

c1 = JD - JD_epoch + (SSN/seconds_per_day)
c2 = c1 / days_per_Julian_century

p1 = 24110.54841
p2 = 8640184.812866
p3 = 0.093104
p4 = (-6.2) * math.pow(10,(-6))

c3 = (p1)+(p2*c2)+(p3*c2*c2)+(p4*c2*c2*c2)+(SSN)-(seconds_per_half_day);

c4 = c3*math.pi/seconds_per_half_day

c5 = c4 % (2*math.pi)

a1 = math.cos(c5)
a2 = math.sin(c5)
a3 = (-1)*a2
a4 = 0
a5 = 1
print()
A = [[a1,a3,a4], [a2,a1,a4], [a4,a4,a5]]

print('Julian date: ' + str(JD_i))
print('\nConverted to rotational matrix: ')
print(A)
