
import math

latgd = 52
lon = 29
alt = 23

R_e= 6378137        
f = 1 / 298.257223563
e = math.sqrt(2 * f - math.pow(f,2))
latgd = latgd * math.pi /180
lon = lon * math.pi / 180

R_e = R_e / math.sqrt(1-(math.pow(e,2) * math.sin(latgd) * math.sin(latgd)))
r_delta=(R_e+alt) * math.cos(latgd);
r_k = ((1-math.pow(e,2)) * R_e + alt) * math.sin(latgd)

r_ecef= [0,0,0]
r_ecef[0]= r_delta *math.cos(lon);
r_ecef[1] = r_delta *math.sin(lon);
r_ecef[2] = r_k;

print(r_ecef)