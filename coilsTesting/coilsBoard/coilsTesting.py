# VERY WIP

import busio
import board

i2c = busio.I2C(board.SCL, board.SDA)
//spi = busio.SPI(board.SCL, )

import digitalio
dirpin = digitalio.DigitalInOut(board.GPIO17) # Chose a direction GPIO pin, need to figure out pin names
dirpin.switch_to_output()

pinmode = False 

while True:
    test_extremes()

    dirpin.value = True
    pinmode = !pinmode
    print(pinmode)


def test_extremes():
    # Code goes here
