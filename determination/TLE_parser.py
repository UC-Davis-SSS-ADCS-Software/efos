
TLE = '1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0 2927  2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537'


info1 = int(TLE[17:20])
info2 = round(float(TLE[20:32]), 4)
info3 = int(TLE[52:59])
info4 = int(TLE[59:61])

info5  = float(TLE[77:86]) # Inclination (degrees)
info6  = float(TLE[86:95]) # RAAN (degrees)

i7_str = TLE[96:103]
in7_str = '0.' + i7_str
info7 = float(in7_str)

info8 = float(TLE[103:112])
info9 = float(TLE[112:121])
info10 = round(float(TLE[121:133]), 4)

info =  [info1, info2, info3, info4, info5, info6, info7, info8, info9, info10]

print('----------------------------')
print('info1: ' + str(info1))
print('info2: ' + str(info2))
print('info3: ' + str(info3))
print('info4: ' + str(info4))
print('info5: ' + str(info5))
print('info6: ' + str(info6))
print('info7: ' + str(info7))
print('info8: ' + str(info8))
print('info9: ' + str(info9))
print('info10: ' + str(info10))
print('info: ')
print(info)
print('----------------------------')





#-------------------------------------------
# IDEAL OUTPUTS FOR GIVEN INPUTS:
#-------------------------------------------

# input: '1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0 2927  2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537'
# 
# output:
# info1: 8
# info2: 264.5178
# info3: -11606
# info4: -4
# info5: 51.6416
# info6: 247.4627
# i7: 0006703
# in7: 0.0006703
# info8: 130.536
# info9: 325.0288
# info10: 15.7213
# 
# ans =
# 
#    1.0e+04 *
# 
#     0.0008    0.0265   -1.1606   -0.0004    0.0052    0.0247    0.0000    0.0131    0.0325    0.0016




# input: '1 43855U 18104G   19056.63241998  .00000042  00000-0  00000-0 0  9998 2 43855  85.0368 131.1811 0018294  19.7011 340.4950 15.22161332 10828'
# 
# output:
# info1: 19
# info2: 56.6324
# info3: 0
# info4: 0
# info5: 85.0368
# info6: 131.1811
# i7: 0018294
# in7: 0.0018294
# info8: 19.7011
# info9: 340.495
# info10: 15.2216
# 
# ans =
# 
#    19.0000   56.6324         0         0   85.0368  131.1811    0.0018   19.7011  340.4950   15.2216