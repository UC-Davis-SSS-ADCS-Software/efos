# General Setup
import time
import board
i2c = board.I2C()

# ESC Setup
import os
os.system ("sudo pigpiod")
import pigpio

# Voltmeter
import adafruit_ina260
Power_Sensor = adafruit_ina260.INA260(i2c)

# IMU
import adafruit_icm20x
IMU = adafruit_icm20x.ICM20948(i2c)

# Connect ESC
ESC = 18
pi = pigpio.pi(); 
pi.set_servo_pulsewidth(ESC, 0)

# ESC Input Range
neutral_ESC_inp = 1488
max_CCW_ESC_inp = 1132
max_CW_ESC_inp = 1832

# Define input parameters
sleep_time = 2.0
input = 50      #(-100 to 100)
[w_x1, w_y1, w_z1] = [0.0, 0.0, 0.0]

# Constant Input Drive Function
def HDD_const_drive(sleep_time, input):
    [w_x0, w_y0, w_z0] = IMU.gyro
    pi.set_servo_pulsewidth(ESC, neutral_ESC_inp + 356 * (input/100))
    time.sleep(sleep_time)

    [w_x1, w_y1, w_z0] = IMU.gyro
    time.sleep(sleep_time)

    [w_xf, w_yf, w_zf] = IMU.gyro
    HDD_current_f = Power_Sensor.current/1000

    HDD_stop()
    
    return [w_x0, w_y0, w_z0, w_x1, w_y1, w_z1, w_xf, w_yf, w_zf, HDD_current_f]
    
# HDD Stop Function
def HDD_stop():
    for i in range(0, 12):
        pi.set_servo_pulsewidth(ESC, neutral_ESC_inp)
        time.sleep(0.5)


if __name__ == "__main__":
    [w_x0, w_y0, w_z0, w_x1, w_y1, w_z1, w_xf, w_yf, w_zf, HDD_current_f] = HDD_cw_drive(sleep_time, input)
    HDD_stop()

    print("Initial Gyro X:%.2f, Y: %.2f, Z: %.2f rads/s" % (w_x0, w_y0, w_z0))
    print("Middle Gyro X:%.2f, Y: %.2f, Z: %.2f rads/s" % (w_x1, w_y1, w_z1))
    print("Final Gyro X:%.2f, Y: %.2f, Z: %.2f rads/s" % (w_xf, w_yf, w_zf))
    print("Nominal Current Draw: %.2f" % (HDD_current_f))
