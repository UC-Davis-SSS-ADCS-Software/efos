# MRW Update 6
# This is an updated version of MRWSystemIDRamp with protection against over-torque
# Based on change of in motor speed, wheel MOI, and motor parameters (max torque), there is a limit on how fast motor can change duty cycle
# Still need to test with rpi

### IMPORTS ###
import RPi.GPIO as GPIO             # calling header file which helps us use GPIOs of RPi
from datetime import datetime       # for formatting data output files
import time                         # calling time to provide delay and timer in program
import os                           # to make new files
import csv                          # to write data to csv
from multiprocessing import Process, Value, Manager # for multi processing
from mpu9250_i2c import *           # import IMU library
import numpy as np                  # for generating inputs
import matplotlib.pyplot as plt     # for plotting results

### GPIO SETUP ###
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

### GLOBAL VARIABLES ###
PWMPin = 19              # PWM output pin
PWMfreq = 96000          # sets PWM Freq to 96kHz
samplefreq = 2           # data sample frequency (Hz)
DIRpin = 4               # direction output pin (+ CCW, - CW)
hallPin = 23             # hall sensor pin
speedFilterWeight = 0.5
maxRatedTorque = 0.45e-3 # motor max rated torque (N m)
MOI = 235.3e-7;          # flywheel MOI (kg m2)
numTachometerTrips = 0   # number of tachometer trips while motor is running
MRW_ON = False           # if motor has been started
manager = Manager()      # manage multiprocessing
DutyCycle = manager.Value('d', 0.0)                            # duty cycle (default 0)
LastDutyCycle = manager.Value('d', 0.0)
currentSpeed = manager.Value('d', 0.0)                         # current speed (default 0)
lastSpeed = manager.Value('d', 0.0)                            # last speed (default 0)
header = ['Duty Cycle', 'Speed', 'Start Time', 'End Time']     # output file header
now = datetime.now()
today = 'WQ' + str(now.month).zfill(2) + str(now.day).zfill(2) + str(now.year)[-2:] + str(now.hour).zfill(2) + str(now.minute).zfill(2)
outputDir= '/home/pi/ADCS_Software/efos/MRWTesting/OutputData'
if os.path.isdir(outputDir) == False:
    os.mkdir(outputDir)
outfile = outputDir + '/speedData' + today + '.csv'

### GPIO PINS ###
GPIO.setup(PWMPin, GPIO.OUT)
GPIO.setup(hallPin, GPIO.IN)
GPIO.setup(DIRpin, GPIO.OUT)

motor = GPIO.PWM(PWMPin,PWMfreq)

### FUNCTIONS ###

# Count tachometer trips
def TachCounter(channel):
    global numTachometerTrips
    numTachometerTrips = numTachometerTrips+1

# Reads IMU and tachometer readings,then calculates speed
# Returns: wx, wy, wz, currentSpeed
def DataRead(start_time,end_time):
    global numTachometerTrips

    delT = end_time - start_time

    #IMU Reading
    try:
        ax,ay,az,wx,wy,wz = mpu6050_conv()
    except:
        ax = 0
        ay = 0
        az = 0
        wx = 0
        wy = 0
        wz = 0

    #Calculate MRW speed (absolute value)
    currentSpeed.value = (numTachometerTrips/delT)*30

    return wx,wy,wz,currentSpeed.value

# Saves data to CSV every 0.5 seconds
def DataSave(DutyCycle):
    global outfile
    global numTachometerTrips
    global MRW_ON

    samplePeriod = 1.0 / samplefreq   # sample period (seconds)
    initTime = time.time()

    print('Data Saving Started')

    while (MRW_ON == True):

        # Record tachometer trips for 0.5 seconds
        try:
            GPIO.add_event_detect(hallPin,GPIO.FALLING,callback=TachCounter) # start counting tachometer trips
            start_time = time.time() - initTime
            time.sleep(samplePeriod)
            end_time = time.time() - initTime
            GPIO.remove_event_detect(hallPin)

        # Error handling - if edge detection fails, motor spins out of control
        # This except statement shuts down the motor.
        # For flight, make sure to return some value to CS to indicate that MRW is shut off
        # TODO: make sure this actually stops the motor
        except:
            motor.stop()
            MRW_ON = False
            break

        # Gather data
        lastSpeed.value = currentSpeed.value
        wx, wy, wz, currentSpeed.value = DataRead(start_time,end_time)
        data = str(DutyCycle.value), currentSpeed.value, start_time, end_time

        # Append data to output file
        with open(outfile, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)
            csvfile.close()

        numTachometerTrips = 0
        print("{} / {}".format(DutyCycle.value, currentSpeed.value))

# Starts MRW
def MRWStart():
    global motor
    global MRW_ON

    motor.start(0.0)
    MRW_ON = True

# Change MRW speed, direction, check for over-torque
def MRWRun(currentDutyCycle):

    # Define new duty cycle
    LastDutyCycle.value = DutyCycle.value
    DutyCycle.value = currentDutyCycle

    # Set direction
    if DutyCycle.value < 0:
        direct = -1
        GPIO.output(DIRpin,GPIO.HIGH)
    elif DutyCycle.value > 0:
        direct = 1
        GPIO.output(DIRpin, GPIO.LOW)

    # Run motor
    startTime = time.time()
    motor.ChangeDutyCycle(abs(DutyCycle.value))
    time.sleep(0.5)     # give motor time to spin up
    endTime = time.time()

    # Check torque
    deltaT = abs(endTime - startTime)
    maxChangeInSpeed = maxRatedTorque * deltaT / MOI
    changeInSpeed = (abs(currentSpeed.value - lastSpeed.value)) * 60 * 2 * np.pi

    if (changeInSpeed > maxChangeInSpeed):

        # Calculate max change in duty cycle that can occur
        changeInDutyCycle = DutyCycle.value - LastDutyCycle.value
        maxChangeInDutyCycle = changeInDutyCycle * (maxChangeInSpeed / changeInSpeed)
        DutyCycle.value = LastDutyCycle.value + maxChangeInDutyCycle

        # Set direction again if we need to, then change duty cycle
        if DutyCycle.value < 0:
            direct = -1
            GPIO.output(DIRpin,GPIO.HIGH)
        elif DutyCycle.value > 0:
            direct = 1
            GPIO.output(DIRpin, GPIO.LOW)
        motor.ChangeDutyCycle(abs(DutyCycle.value))

        # Now we give it a moment to spin up
        # Then try to run at our desired duty cycle again, until we are no longer exceeding max torque
        MRWRun(currentDutyCycle)

# Set up output file
def CreateOutputFile():
    global outfile

    with open(outfile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        csvfile.close()


#### MAIN ####
def main():
    global MRW_ON
    global DutyCycle

    # Turn on motor
    print("Starting...")
    if (MRW_ON == False):
        MRWStart()

    # Start data saving
    CreateOutputFile()
    p = Process(target=DataSave, args=(DutyCycle,))
    p.start()

    # Set up ramp parameters
    allDutyCycles = np.linspace(0, 100, 11)     # absolute value of duty cycles (0-100)
    timePerDutyCycle = 10                       # time to run each duty cycle (seconds)

    # Run ramp
    for currentDutyCycle in allDutyCycles:
        MRWRun(currentDutyCycle)
        time.sleep(timePerDutyCycle)

    # cleanup/shutdown
    time.sleep(2) # idk if we still need this line but i'm not gonna delete it
    GPIO.remove_event_detect(hallPin)
    motor.stop()
    MRW_ON = False
    p.terminate()
    p.join()
    GPIO.cleanup()
    print('done')

    # Plot result
    rpm, secondsElapsed = np.loadtxt(outfile, unpack=True, skiprows=1, delimiter=',', usecols=(1,2))
    plt.plot(secondsElapsed, rpm)
    plt.title('Time vs RPM')
    plt.xlabel('Time (s)')
    plt.ylabel('RPM')
    plt.grid()
    plt.show()

if __name__ == '__main__':
    main()
