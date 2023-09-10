# VERY WIP
# Import packages
import busio
import board
import spidev
import RPi.GPIO as GPIO
import time

# Set up I2C and SPI
i2c = busio.I2C(board.SCL, board.SDA)
spi = spidev.SpiDev()
spi.open(0,0) 

spi.max_speed_hz = 7629

# Set up direction pin
dirpin = 17

GPIO.setup(dirpin, GPIO.OUT)
pinmode = False
GPIO.output(dirpin, GPIO.LOW)

# Function for testing extreme 
def test_extremes():

    # Need to convert pot values to hex (pi does not use 0-255)

    print("0")
    writePot(0)
    time.sleep(2)

    print("127")
    writePot(127)
    time.sleep(2)

    print("255")
    writePot(255)
    time.sleep(2)

# Write an integer as a 2-byte array to send via SPI (range 0-255)
def writePot(input):
    # figure out hex thing 
    msb = input >> 8    # most significant bit (first 8 bits)
    lsb = input & 0xFF  # least significant bit (last 8 bits) (0-255 where 0xFF is 255)

    spi.xfer([msb, lsb])

while True:
    test_extremes()
    pinmode = not pinmode
    if (pinmode == False):
        GPIO.output(dirpin, GPIO.LOW)
    else:
        GPIO.output(dirpin, GPIO.HIGH)
    print(pinmode)