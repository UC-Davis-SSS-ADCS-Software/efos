from astropy import coordinates
from datetime import datetime
import numpy as np
from astropy.time import Time

# INPUTS: current datetime, as in Python datetime package
# OUTPUTS: unit vector pointing to sun in inertial reference frame
def sunLookup(currentDatetime):
    t = Time(str(currentDatetime)) # convert to astropy time package
    sun_gcrs = coordinates.get_sun(t) # get sun coordinates
    s_eci = np.array([sun_gcrs.cartesian.x.value, sun_gcrs.cartesian.y.value, sun_gcrs.cartesian.z.value]) # represent sun in X, Y, Z
    s_eci_normalized = s_eci / np.linalg.norm(s_eci) # convert to unit vector
    return s_eci_normalized
