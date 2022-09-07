import math

def calendar_date_to_JD(date):
    # date = [year, month, day, hr, mins, sec]

    Y = date[0]
    M = date[1]
    D = date[2]
    hr  = date[3]
    mins = date[4]
    sec = date[5]


    #INPUT: Calendar date, MM,DD,YYYY
    #OUTPUT: Modified Julian Date, MJD
    #source: Montenbruck A.1.1 page 321


    if Y < 1583:
        print('Error, year is out of bounds.')
        JD = 0
    else:
        if M <= 2:
          y = Y-1
          m = M+12
        else:
          y = Y;
          m = M;

        B = math.floor(y/400) - math.floor(y/100) + math.floor(y/4)

        MJD = 365*y - 679004 + math.floor(B) + math.floor(30.6001*(m+1)) + D + hr/24 + mins/(24*60) + sec/(24*60*60)

        JD = MJD + 2400000.5

        print(str(date[0]) + '/' + str(date[1]) + '/' + str(date[2]))
        print('hrs: ' + str(date[3]) + ', mins: ' + str(date[4]) + ', secs: ' + str(date[5]))
        print('---->')
        print(JD)
        return JD

