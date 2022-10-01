#*******************************************************************************#
#PURPOSE:                                                                       #
# wheelSpeedControllerWithPi combines MRWTest_v7 and Wheel_SpeedController      #
# so that the motor runs based on a calculated torque command                   #
# For now, the torque command is received by user input, but will eventually be #
# connected to a controller.                                                    #
# Authors: Chris Andrade, Victoria De La Torre, Natasha Evans, Jassan Gill,     #
#          Anjali, Gupta, Dzuy Nguyen                                           #
#*******************************************************************************#

#*******************************************************************************#
#RPi-MRW SETUP:                                                                 #
# RPi is used to power the direction pin and PWM signal pin.                    #
# The motor will need to have a separate power source.                          #
# Ensure that the RPi and Power Source have common ground.                      #
# Refer to the Drive for how to connect all of the wires.                       #
#*******************************************************************************#

#Import Libraries
import RPi.GPIO as GPIO             # calling header file which helps us use GPIOs of RPi
import time                         # calling time to provide delay and timer in program
import os                           # to make new files
import csv                          # to write data to csv
import threading                    # for multi threading, used for taking in new speed commands
from mpu9250_i2c import *           # import IMU library
import Wheel_Speed_Controller

print('Libraries Loaded.')

#Common GPIO setup after importing the library
GPIO.setwarnings(False)                   # do not show any warnings
GPIO.setmode(GPIO.BCM)                    # we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)

#*********************************Functions Used********************************#
#Interrupt Service to Count Hall Sennsor Trips
def TachCounter(channel):
    global numTachometerTrips
    numTachometerTrips = numTachometerTrips+1

#Interrupt Service to Update MRW desired torque
def inputloop():
    print('Input loop started')
    while True:
        global desiredTorque
        desiredTorque = float(input()) # update this so instead of receiving input from terminal, it receives it from controller. May need to write new controller for fishing line testing
        print('Desired Torque set to ' + str(desiredTorque))
        time.sleep(0.2)

#Create new csv file
def createCSV(path):
    path = str(path)    # Ensures the path is a string
    os.mkdir(path)      # Creates new directory with that path name
    header = ['Desired Torque', 'Duty Cycle','wx','wy','wz','Current Speed','Start Time','End Time']    # Change the header columns as needed
    with open(path,'w', newline='') as csvfile:     # Opens csv file, writes the header
        writer = csv.writer(csvfile)
        writer.writerow(header)

#Reads IMU and tachometer readings,then calculates speed
def data_read(start_time,end_time):
    global numTachometerTrips
    global direct

    delT = end_time - start_time

    #IMU Reading
    try:
        ax,ay,az,wx,wy,wz = mpu6050_conv()
    except:
        pass

    #Calculate MRW speed
    currentSpeed = direct*((numTachometerTrips/delT)*30)

    return wx,wy,wz,currentSpeed    #These values are needed for the main loop

#Writes data to csv
def data_write(filename,data):
    #Row of data must be finalized before calling this function. Cannot append to the same/existing row
    #Create csv file
    #If the directory already exists, it will continue
    filename = str(filename)    # Ensures the filename is a string
    path = '/home/pi/MRW Codes/Data/' + filename

    # try to create the new csv files, if it already exists it will continue
    try:
        createCSV(path)
    except:
        pass

    #Opens csv file and writes the new line of data
    with open(path,'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

print('Functions Setup.')

#****************************Variables and Pins Setup****************************#
PWMPin = 19
PWMfreq = 96000                             # sets PWM Freq to 96kHz
DIRpin = 4
DutyCycle = 0
desiredTorque = 0
hallPin = 23
speedFilterWeight = 0.5
numTachometerTrips = 0
maxMRWSpeed = 4188                          # need to check value with wheel on motor

#Pin Setup
GPIO.setup(PWMPin,GPIO.OUT)                 # initialize GPIO19 - PWMPin as an output
GPIO.setup(hallPin,GPIO.IN)                 # initialize GPIO23 - hallPin as an input
GPIO.setup(DIRpin,GPIO.OUT)                 # initialize GPIO4 - DIRpin as an output

print('Variables and Pins Setup Complete.')

#*************************Attach Interrupt and Motor Setup************************#
GPIO.add_event_detect(hallPin,GPIO.FALLING,callback=TachCounter)
motor = GPIO.PWM(PWMPin,PWMfreq)            # Specify GPIO19 as PWM output with 96kHz frequency
input_thread = threading.Thread(target = inputloop)

print('Interrupt Attached and Motor Setup.')
print('All Setup Complete.')

#********************************** M A I N **************************************#
print('Start')

while(True):

    if abs(DutyCycle) > 0:      # If we command the motor to start moving, then it has been activated
        activate = True

    #If-else to determine direction sign and turn on direction pin if needed
    if DutyCycle < 0:
        direct = -1
        GPIO.ouput(DIRpin,GPIO.HIGH)
    elif DutyCycle > 0:
        direct = 1
        GPIO.output(DIRpin,GPIO.LOW)

    if activate == True and desiredTorque == float("NaN"):     # If the motor is running and we command an invalid torque, it will exit the while loop
        break

    duty_cycle = abs(DutyCycle)     # GPIO can only command a positive duty cycle
    start_time = time.time()
    motor.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)                 # This delay, for the most part, will determine the operating freq of the data reading
    end_time = time.time()

    wx,wy,wz,currentSpeed = data_read(start_time,end_time)

    data = desiredTorque,DutyCycle,wx,wy,wz,currentSpeed,start_time,end_time
    data_write('filename',data)

    numTachometerTrips = 0
    lastSpeed = currentSpeed
    GPIO.add_event_detect(hallPin,GPIO.FALLING,callback=TachCounter)

    # calculate new duty cycle
    desiredSpeed = Wheel_Speed_Controller.wheelSpeedController(desiredTorque, lastSpeed, float(end_time) - float(start_time))
    DutyCycle = 100 * desiredSpeed / maxMRWSpeed
    # edge case where duty cycle is slightly greater than 100 or less than -100
    if (DutyCycle < -100):
        DutyCycle = - 100
    elif (DutyCycle > 100):
        DutyCycle = 100

#Clean up and shut down
time.sleep(2)
GPIO.remove_event_detect(hallPin)
motor.stop()
GPIO.cleanup()
print('Done')







