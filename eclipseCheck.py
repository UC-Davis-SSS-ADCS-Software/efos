# Where the sun don't shine - Checking for eclipse
#
# Eclipse check function will take an array input for sun sensor values, compare it,
# and spit out total number of sensors (out of 24) considered to be
# "in eclipse" troug the variable inEclipse.
#
# Yuvraj Jadav
#
#-----------------------------------------------------------------------------------

# The actual eclipse check function:
def eclipseCheck(valueArray, limit):
    total = 0
    for x in valueArray:
        if x <= limit:
            total += 1
    return total


# Used actual python 
def main():
    
    sunSensorValues = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
    threshold = 0.8

    # ¡DON'T FORGET TO ASSIGN IT TO A VARIABLE WHEN YOU CALL THE FUNCTION!
    # inEclipse variable should have a count of the sensors "in eclipse" (out of 24).
    inEclipse = eclipseCheck(sunSensorValues, threshold)

    # Printing the variable for the human. I assume this will be
    # unnecessary in actual use.
    print(inEclipse)


if __name__ == "__main__":
    main()

#-----------------------------------------------------------------------------------


