# Where the sun don't shine - Compare values from the sun sensors to a tresold to determine
# if the cubesat is in eclipse or not

#-----------------------------------------------------------------------------------

# Inputs wich will be imported in somehow. These are random values.
# I'm assuming there will be a lot more decimals places? I've kept it simple for now.
sunSensorValues = [0.5, 0.6, 0.7, 0.8, 0.9, 0.1, 0.2, 0.3, 0.7, 0.7]


# Value to measure against. The sun gods will probably tell us sooner or later right?
eclipseThreshold = 0.5

# Our variables that will do the counting for us
eclipse = 0
sunTan = 0

# Checking the values against the threshold and tallying
for x in sunSensorValues:
    if x <= eclipseThreshold:
        eclipse += 1
    else:
        sunTan += 1


# Printing the values out for the human. I'm assuming there won't be a need for this
# and the values will just be fed to te next program in the chain.
print("\nSensors in eclipse:", eclipse)
print("Sensors being baked:", sunTan)
print("\nThe average sensor value is", (sum(sunSensorValues)/len(sunSensorValues)),
      "and the given threshold value is", str(eclipseThreshold)+"." )

#-----------------------------------------------------------------------------------


