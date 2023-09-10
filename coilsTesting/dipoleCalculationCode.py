from icm20948 import ICM20948
import adafruit_icm20x
import time
import board
import math

print("Rotate 360 deg")

X=0
Y=1
Z=2

AXES = Y,Z
i2c = board.I2C() # uses board.SCL and board.SDA
imu = adafruit_icm20x.ICM20948(i2c)

amin = list(imu.magnetic)
amax = list(imu.magnetic)

while True:
	mag = list(imu.magnetic)
	for i in range(3):
		v = mag[i]
		if v < amin[i]:
			amin[i] = v
			
		if v > amax[i]:
			amax[i] = v
			
		mag[i] -= amin[i]
		
		try:
			mag[i] /= amax[i] - amin[i]
		except ZeroDivisionError:
			print("Go to HELL")
			pass
		
		mag[i] -= 0.5
		
	heading = math.atan2(mag[AXES[0]], mag[AXES[1]])
	if heading < 0:
		heading += 2*math.pi
	heading = math.degrees(heading)
	heading = round(heading)
	print("Heading: {}".format(heading))
	time.sleep(0.1)
