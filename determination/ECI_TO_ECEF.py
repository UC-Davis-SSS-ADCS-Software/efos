import datetime
import math
import numpy as np

t_jd = [2021, 12, 27, 14, 35, 22]
# t_jd = [year, month, day, hour, minute, second]

year = t_jd[0]
month = t_jd[1]
day = t_jd[2]
hour = t_jd[3]
minute = t_jd[4]
second = t_jd[5]

def get_julian_datetime(date):

    # Ensure correct format
    if not isinstance(date, datetime.datetime):
        raise TypeError('Invalid type for parameter "date" - expecting datetime')
    elif date.year < 1801 or date.year > 2099:
        raise ValueError('Datetime must be between year 1801 and 2099')

    # Perform the calculation
    julian_datetime = 367 * date.year - int((7 * (date.year + int((date.month + 9) / 12.0))) / 4.0) + int(
        (275 * date.month) / 9.0) + date.day + 1721013.5 + (date.hour + date.minute / 60.0 + date.second / math.pow(60,
        2)) / 24.0 - 0.5 * math.copysign(1, 100 * date.year + date.month - 190002.5) + 0.5
    
    return julian_datetime

date_time = datetime.datetime(year, month, day, hour, minute, second) # (year, month, day, hour, minute, second)
JD_current = get_julian_datetime(date_time)
print("Julian Date, Actual:", JD_current)

J_2000 = 2451545.0 # Julian Date at 2000 Jun, 1 12h UT1

# calculate Julian Date for the beginning of the day
date_GMST = datetime.datetime(date_time.year, date_time.month, date_time.day, 0, 0, 0)
JD = get_julian_datetime(date_GMST)
print("Julian Date, Beginning of Day:", JD)

# calculate Greenwich Mean Sidereal Time (GMST)
d_0 = JD - J_2000 # Juliean days since J2000
T_u = d_0/36525 # Juliean centuries 
theta_g = 24110.54841 + 8640184.812866 * T_u + 0.093104 * T_u ** 2-6.2 * 10 ** (-6) * T_u ** 3
w = (7.2921158553 * 10 ** (-5) + 4.3 * 10 ** (-15) * T_u) * (86400 / (2 * math.pi)) # Earth's rotation rate in [sidereal second/UT second]
t = date_time.hour * 3600 + date_time.minute * 60 + date_time.second
GMST = theta_g + w * t
GMST_mod = GMST % 86400 # [seconds]
print("GMST for the Day [seconds]:", GMST_mod)
conversion_GMST = datetime.timedelta(seconds=GMST_mod)
GMST_time = str(conversion_GMST)
print("GMST Time:", GMST_time)

# calculate degrees
degrees_GMST = (GMST_mod/86400)*360
print("GMST Degrees:", degrees_GMST)

# create rotation matrix
c = math.cos(math.radians(degrees_GMST))
s = math.sin(math.radians(degrees_GMST))
R_eci2ecef = np.array([[c,s,0], [-s,c,0], [0,0,1]])
print("Rotation Matrix:")
print(R_eci2ecef)
