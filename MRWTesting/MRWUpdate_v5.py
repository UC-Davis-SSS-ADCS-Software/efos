# MRW Update 5
# UPDATES: plots speed vs time to characterize speed at different duty cycles
# UPDATES: no modes, only runs at a constant speed. This version is simplified from v4; v4 may be more useful in developing flight code
# TODO: (eventually) run w/o internet connection to verify that libraries are ok
# TODO: detect ccw vs cw motor spin

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
numTachometerTrips = 0   # number of tachometer trips while motor is running
MRW_ON = False           # if motor has been started
manager = Manager()      # manage multiprocessing
DutyCycle = manager.Value('d', 0.0)                                             # duty cycle (default 0)
header = ['Duty Cycle', 'wx', 'wy' 'wz', 'Speed', 'Start Time', 'End Time']     # output file header
outfile = '/home/pi/MRW_Codes/Data/speedDataDefault.csv'                        # output file name - will be defined at motor start


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
def DataRead(start_time,end_time):
    global numTachometerTrips

    delT = end_time - start_time
    
    #IMU Reading
    try:
        ax,ay,az,wx,wy,wz = mpu6050_conv()
    except:
        pass

    #Calculate MRW speed (absolute value)
    currentSpeed = (numTachometerTrips/delT)*30

    return wx,wy,wz,currentSpeed

# Saves data to CSV
# TODO: find a way to determine ion based on actual spin direction and not applied duty cycle (MRW takes time to switch directions)
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
        wx,wy,wz,currentSpeed = DataRead(start_time,end_time)
        data = str(DutyCycle.value), wx, wy, wz, currentSpeed, start_time, end_time
    
        # Append data to output file
        with open(outfile, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)
            csvfile.close()
    
        numTachometerTrips = 0
        print("{} / {}".format(DutyCycle.value, currentSpeed))

# Starts MRW
def MRWStart():
    global motor
    global MRW_ON
    
    motor.start(0.0)
    MRW_ON = True
    
# Set up output file
def CreateOutputFile():
    global outfile
    
    now = datetime.now()
    today = 'WQ' + str(now.month).zfill(2) + str(now.day).zfill(2) + str(now.year)[-2:] + str(now.hour).zfill(2) + str(now.minute).zfill(2)
    outfile = '/home/pi/MRW_Codes/Data/speedData' + today + '.csv'
    with open(outfile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        csvfile.close()
    
#### MAIN ####
def main():
    global MRW_ON
    global DutyCycle
    
    # Turn on motor
    if (MRW_ON == False):
        MRWStart()
            

    # Get runtime
    runtime = input("Runtime (s): ")
    try:
        runtime = int(runtime)
    except:
        runtime = 20
        print("Default 20 second run time.")
    
    # Get duty cycle
    d = input("Constant Duty Cycle: ")
    try:
        DutyCycle.value = float(d)
    except:
        DutyCycle.value = 50
        print("Default to 50% duty cycle CCW.")
        
    # Start data saving
    startTime = time.time()
    CreateOutputFile()
    p = Process(target=DataSave, args=(DutyCycle,))
    p.start()
        
    # If-else to determine direction sign and turn on direction pin if needed
    if DutyCycle.value < 0:
        direct = -1
        GPIO.output(DIRpin,GPIO.HIGH)
    elif DutyCycle.value > 0:
        direct = 1
        GPIO.output(DIRpin,GPIO.LOW)
        
    # Set duty cycle
    motor.ChangeDutyCycle(abs(DutyCycle.value))
    time.sleep(runtime)
        
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
    rpm, secondsElapsed = np.loadtxt(outfile, unpack=True, skiprows=1, delimiter=',', usecols=(4,5))
    plt.plot(secondsElapsed, rpm)
    plt.title('Time vs RPM')
    plt.xlabel('Time (s)')
    plt.ylabel('RPM')
    plt.grid()
    plt.show()
    
if __name__ == '__main__':
    main()
    
