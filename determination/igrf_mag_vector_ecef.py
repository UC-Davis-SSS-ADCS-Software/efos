# imports
import pyIGRF, datetime
import numpy as np
from astropy.coordinates import EarthLocation
from astropy import units as u

R_e = 6371 # mean radius of Earth

#INPUTS: x_ecef: position in km in ecef frame, [x y z]
# Note sign convention: latitude is positive in the north direction, longitude is positive in the east direction
#INPUTS: t_jd: julian date (days since noon on Jan 1 2000)
#OUTPUT: B_ecef: magnetic field in microtesla
def igrf_mag_vector_ecef(x_ecef, t_jd):
    
    # convert ecef to latitude and longitude
    xq = u.quantity.Quantity(x_ecef[0], u.km)
    yq = u.quantity.Quantity(x_ecef[1], u.km)
    z1 = u.quanity.Quantity(x_ecef[2], u.km)
    loc = EarthLocation(x=xq,y=yq,z=zq)
    longitude, latitude, altitude = loc.to_geodetic()
    lon = longitude.value # longitude in degrees
    lat = latitude.value # latitude in degrees
    alt = (altitude.value / 1000) - R_e # altitude in km
    
    # get decimal date
    delta = datetime.timedelta(days = t_jd) # convert julian date to delta in days
    d = datetime.datetime(2000,1,1,12,0,0) + delta # will depend on epoch -- currently using jd2000
    decimal_date = (float(d.strftime("%j"))-1) / 366 + float(d.strftime("%Y"))
    
    # get magnetic field in ecef frame
    r = pyIGRF.igrf_value(lat, lon, alt, decimal_date) # get magnetic field parameters
    vector = np.array([r[3], r[4], r[5]]) # save north, east, and vertical components of magnetic field in nT
    mag_vector_ecef = vector / np.linalg.norm(vector) # normalize
    return mag_vector_ecef

