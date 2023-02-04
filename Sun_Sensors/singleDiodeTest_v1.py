# Import packages
import board            # Raspberry pi
import busio            # supports serial communication such as i2c
import time as t
import math as m
i2c = busio.I2C(board.SCL, board.SDA)       # set up i2c communication

import adafruit_ads1x15.ads1115 as ADS   # analog to digital converter

from adafruit_ads1x15.analog_in import AnalogIn


# Map a value from one range to another (such as 0-1 to 0-100)
# Oldval --> value to map to a new range
# Oldmin, Oldmax --> limits of old range
# Newmin, Newmax --> limits of new range
def map(oldval, oldmin, oldmax, newmin, newmax):
    return((((oldval - oldmin) * (newmax - newmin)) / (oldmax - oldmin)) + newmin)

# Additional variables
ads = ADS.ADS1115(i2c)
volt_list=[]
deg_list=[]
pres = 10
i=0

# Sensor reading range (needs calibration)
sensorMin = 2.4800756859
sensorMax = 3.080093997

# Desired reading range - we want to return a value from 0 to 1
mappedMin = 0
mappedMin = 1

# Read voltages from sun diodes  and save to list of values
while i < 500:

    # For single diode test, only read one channel
    chan0 = round(AnalogIn(ads, ADS.P0).voltage,pres)
    chan1 = 0#round(AnalogIn(ads, ADS.P1).voltage,p)
    chan2 = 0#round(AnalogIn(ads, ADS.P2).voltage,p)
    chan3 = 0#round(AnalogIn(ads, ADS.P3).voltage,p)

    # Map from sensor range to 0-1
    mapped=map(chan0, sensorMin, sensorMax, mappedMin, mappedMax)

    # Save reading to list of voltages
    volt_list.append(chan0)

    # Convert to degrees
    #deg=m.degrees(m.acos(mapped))
    #deg_list.append(deg)

    # Display results
    print(f"{chan0}\t")

    # Wait before next loop, increment, and take another reading
    t.sleep(.1)
    i+=1

# Save voltage results to a file
with open("data6_raw_attempt2.txt","w") as external_file:
    print(volt_list,file=external_file)
    external_file.close()

# Save angle results for a file (TODO: put all of this in one file and uncomment this section!)
#with open("data6_mapped.txt","w") as external_file:
#    print(deg_list,file=external_file)
#   external_file.close()
