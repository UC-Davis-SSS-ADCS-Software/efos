#*******************************************************************************#
#PURPOSE:                                                                       #
# MRWtest_v7 will restructure the MRW test script series. The main goal is to   #
# separate the data collection from the motor speed commanding.                 #
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
# Updates 11/6/22:
# Switched to multiprocessing
# Thanks StackOverflow!
# Reference: https://stackoverflow.com/questions/49439139/manipulating-raspbery-pis-dc-motor-speed-while-running-gui
# TODO Before running on Pi: figure out how to read returned values from processes and terminate processes when duty cycle = 0
# TODO Before running on Pi: test GUI loop and make sure that doesn't crash

#Import Libraries
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QInputDialog, QLineEdit,QFileDialog
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtGui import QIcon
import RPi.GPIO as GPIO             # calling header file which helps us use GPIOs of RPi
import time                         # calling time to provide delay and timer in program
#import numpy as np                 # unused so far but feel free to uncomment if used
#import sys                         # also unused
import os                           # to make new files
import csv                          # to write data to csv
from multiprocessing import Process, Queue, Value             # used for taking in new speed commands
from mpu9250_i2c import *           # import IMU library

print('Libraries Loaded.')

#Common GPIO setup after importing the library
GPIO.setwarnings(False)                   # do not show any warnings
GPIO.setmode(GPIO.BCM)                    # we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)

#*********************************Functions Used********************************#
# Set up GUI
app = QtWidgets.QApplication([])
dlg = uic.loadUi('Motor.ui')

# Change motor speed
def changeMotorSpeed():
    dlg.label.setText(str(dlg.slider.value()))
    print('Duty Cycle set to ' + str(DutyCycle))
    file = open('dutyCycles.txt')
    file.write(str(DutyCycle))
    file.close()
    time.sleep(0.2)

#Interrupt Service to Count Hall Sennsor Trips
def TachCounter(channel):
    global numTachometerTrips
    numTachometerTrips = numTachometerTrips+1

#Create new csv file
def createCSV(path):
    path = str(path)    # Ensures the path is a string
    os.mkdir(path)      # Creates new directory with that path name
    header = ['Duty Cycle','wx','wy','wz','Current Speed','Start Time','End Time']    # Change the header columns as needed
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

# Run GUI
def runProgram():
    dlg.show()
    app.exec()

# Update speed when slider changes
dlg.slide.valueChanged.connect(changeMotorSpeed)

print('Functions Setup.')

#****************************Variables and Pins Setup****************************#
PWMPin = 19                                 
PWMfreq = 96000                             # sets PWM Freq to 96kHz
DIRpin = 4
DutyCycle = 0
hallPin = 23
speedFilterWeight = 0.5
numTachometerTrips = 0

#Pin Setup
GPIO.setup(PWMPin,GPIO.OUT)                 # initialize GPIO19 - PWMPin as an output
GPIO.setup(hallPin,GPIO.IN)                 # initialize GPIO23 - hallPin as an input
GPIO.setup(DIRpin,GPIO.OUT)                 # initialize GPIO4 - DIRpin as an output

print('Variables and Pins Setup Complete.')

#*************************Attach Interrupt and Motor Setup************************#
GPIO.add_event_detect(hallPin,GPIO.FALLING,callback=TachCounter)
motor = GPIO.PWM(PWMPin,PWMfreq)            # Specify GPIO19 as PWM output with 96kHz frequency

print('Interrupt Attached and Motor Setup.')
print('All Setup Complete.')

#********************************** M A I N **************************************#
print('Start')

def runMotor():
    global numTachometerTrips
    try:
        file = open('dutyCycle.txt', 'r')
        DutyCycle = int(file.read())
        file.close()
        if abs(DutyCycle) > 0:      # If we command the motor to start moving, then it has been activated
            activate = True

        #If-else to determine direction sign and turn on direction pin if needed
        if DutyCycle < 0:
            direct = -1
            GPIO.ouput(DIRpin,GPIO.HIGH)
        elif DutyCycle > 0:
            direct = 1
            GPIO.output(DIRpin,GPIO.LOW)

        if activate == True and DutyCycle == 0:     # If the motor is running and we command a 0, it will exit the while loop
            return 1    # turning off motor

        DutyCycleAbs = abs(DutyCycle)     # GPIO can only command a positive duty cycle
        start_time = time.time()
        motor.ChangeDutyCycle(DutyCycleAbs)
        time.sleep(0.5)                 # This delay, for the most part, will determine the operating freq of the data reading
        end_time = time.time()

        wx,wy,wz,currentSpeed = data_read(start_time,end_time)

        data = DutyCycle,wx,wy,wz,currentSpeed,start_time,end_time
        data_write('filename',data)

        numTachometerTrips = 0
        GPIO.add_event_detect(hallPin,GPIO.FALLING,callback=TachCounter)
    except:
        return 2    # error running main loop
    return 0    # no errors, keep running code

#Clean up and shut down
def End():
    time.sleep(2)
    GPIO.remove_event_detect(hallPin)
    motor.stop()
    GPIO.cleanup()
    print('Done')

if __name__ == 'main':
    p1 = Process(target=runMotor, args=())
    p2 = Process(target=runProgram, args=())

    p1.start()
    p2.start()

    p1.join()
    p2.join()
    






