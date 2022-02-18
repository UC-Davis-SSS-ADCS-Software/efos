# sunsensor test with python

#library imports
import numpy as np
import RPi.GPIO as GPIO
import time
import math as m

#arrays for x,y,z dimensions
e1 = []
e2 = []
e3 = []
x = 0.0
y = 0.0
z = 0.0
angle_param  = [e1,e2,e3]
#notational array
labels = ['x','y','z','X','Y','Z','e1','e2','e3']


#Input/Output code used as reccomended from https://github.com/pimylifeup/Light_Sensor/blob/master/light_sensor.py 
GPIO.setmode(GPIO.BOARD)

#define the pin that goes to the circuit
pin_to_circuit = 17
#input(int(pin_to_circuit))
def rc_time (pin_to_circuit):
    count = 0
  
    #Output on the pin for 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1

    return count

#Catch when script is interupted, cleanup correctly
try:
    # Main loop
    while True:
        print(rc_time(pin_to_circuit))
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()



# back to club code:
# general testing function
def test(V0,x,y,z,angular, axis,labels):
    return 1
#Function: Converts Euler Angles to Quaterninons
def Euler2Quats(angle_param):
    
    phi = angle_param[0]
    theta = angle_param[1]
    psi = angle_param[2]

    q0 = np.cos(phi/2)*np.cos(theta/2)*np.cos(psi/2) + np.sin(phi/2)*np.sin(theta/2)*np.sin(psi/2)
    q1 = np.sin(phi/2)*np.cos(theta/2)*np.cos(psi/2) - np.cos(phi/2)*np.sin(theta/2)*np.sin(psi/2)
    q2 = np.cos(phi/2)*np.sin(theta/2)*np.cos(psi/2) + np.sin(phi/2)*np.cos(theta/2)*np.sin(psi/2)
    q3 = np.cos(phi/2)*np.cos(theta/2)*np.sin(psi/2) - np.sin(phi/2)*np.sin(theta/2)*np.cos(psi/2)

    q = np.array([q0,q1,q2,q3])

    return q

testing = True

# measured vectors
sun_Values = np.array([angle_param[0], angle_param[1],angle_param[2]])
acc_Values = np.array([0.02, -0.98, 0.19])

# input Euler angle rotations
roll = np.radians(e1)
pitch = np.radians(e2)
yaw = np.radians(e3)
angular = np.array([roll,pitch,yaw])
print("Woodsat Euler Angles as Roll, Pitch,and Yaw")
print(np.degrees(angular))

# Theoretically calculated quaternion
Thy_Quat = Euler2Quats(angle_param)
print("Expected Quaternion: ", Thy_Quat)


# reference vectors (hmmmmm)

# compute attitude
pyramids = 6
testing = True
while (testing):
    while(pyramids<=6):
        while (n<4):
            GPIO.input(pin_to_circuit) == GPIO.LOW
            GPIO.write(GPIO.LOW)
            a = GPIO.LOW


print("The Attitude is Determined to be: ", attitude)


#Add a function that reads-in the measurements without being the same function that calculates stuff
# compute angle/position error 


#
#
#File Output to be saved as a csv
# need to write calculated data to testing document. 
# add this code to github? 
# add this code to the drive?
#

#
# BELOW: Mathematical Functions for reference and use if necessary
#
#Rotation Matricies as Functions of an angle Theta
def Rx(theta):
  return np.matrix([[ 1,0,0 ],[0,m.cos(theta),-m.sin(theta)],[0,m.sin(theta),m.cos(theta)]])
  
def Ry(theta):
  return np.matrix([[ m.cos(theta), 0, m.sin(theta)],[0,1,0],[-m.sin(theta), 0, m.cos(theta)]])
  
def Rz(theta):
  return np.matrix([[ m.cos(theta),-m.sin(theta),0],[ m.sin(theta),m.cos(theta),0],[0,0,1]])
#Euler Angles to and from 
def EulerAngleExample(Rx,Ry,Rz):
    phi = m.pi/2
    theta = m.pi/4
    psi = m.pi/2
    print("phi =", phi)
    print("theta  =", theta)
    print("psi =", psi)
  
  
    R = Rz(psi) * Ry(theta) * Rx(phi)
    print(np.round(R, decimals=2)) 
    import sys
    tol = sys.float_info.epsilon * 10
  
    if abs(R.item(0,0))< tol and abs(R.item(1,0)) < tol:
        eul1 = 0
        eul2 = m.atan2(-R.item(2,0), R.item(0,0))
        eul3 = m.atan2(-R.item(1,2), R.item(1,1))
    else:   
        eul1 = m.atan2(R.item(1,0),R.item(0,0))
        sp = m.sin(eul1)
        cp = m.cos(eul1)
        eul2 = m.atan2(-R.item(2,0),cp*R.item(0,0)+sp*R.item(1,0))
        eul3 = m.atan2(sp*R.item(0,2)-cp*R.item(1,2),cp*R.item(1,1)-sp*R.item(0,1))
