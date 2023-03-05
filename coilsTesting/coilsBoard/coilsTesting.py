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
GPIO.setup(dirpin, GPIO.setup)
pinmode = False
GPIO.output(dirpin, GPIO.LOW)
def test_extremes():
    print("0")
    writePot(0)
    time.sleep(2)

    print("127")
    writePot(127)
    time.sleep(2)

    print("255")
    writePot(255)
    time.sleep(2)

# Write an integer as a 2-byte array to send via SPI
def writePot(input):
    msb = input >> 8    # most significant bit
    lsb = input & 0xFF  # least significant bit
    spi.xfer([msb, lsb])

while True:
    test_extremes()
    pinmode = not pinmode
    if (pinmode == False):
        GPIO.output(dirpin, GPIO.LOW)
    else:
        GPIO.output(dirpin, GPIO.HIGH)
    print(pinmode)