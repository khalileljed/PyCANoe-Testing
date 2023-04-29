from math import ceil
import time
import ast

import CANoe
import helper

# Parameters
'''config = helper.read_config()

ZERO_POS = float(config['spoiler positions']['zero_pos'])
ECO_POS = float(config['spoiler positions']['eco_pos'])
PERFO_POS = float(config['spoiler positions']['perfo_pos'])

Tolerance = float(config['spoiler positions']['tolerance'])

DM_normal = int(config['Drivemodes']['dm_normal'])
DM_sport = int(config['Drivemodes']['dm_sport'])
DM_sportplus = int(config['Drivemodes']['dm_sportplus'])
DM_offroad = int(config['Drivemodes']['dm_offroad'])

AERO_SETUP = ast.literal_eval(config['Signals']['aero_setup'])
ACTUAL_POS = ast.literal_eval(config['Signals']['actual_pos'])
ACTUAL_SPEED = ast.literal_eval(config['Signals']['actual_speed'])
LAUNCH = ast.literal_eval(config['Signals']['launch'])
DriveMode = ast.literal_eval(config['Signals']['drivemode'])
AERO_1_ERROR = ast.literal_eval(config['Signals']['aero_1_error'])
SUNROOF_POS = ast.literal_eval(config['Signals']['sunroof_pos'])
SUNROOF_LAGE = ast.literal_eval(config['Signals']['sunroof_lage'])'''

'''app = CANoe.CanoeSync()

if app == None:
    app.Load(
        r"\Projects\Spoiler\CANoe_Simulation_SX_400_v6.3\01_Configuration\HCP4_v13_Testing.cfg")
else:
    app.Stop()
    app.Load(
        r"\Projects\Spoiler\CANoe_Simulation_SX_400_v6.3\01_Configuration\HCP4_v13_Testing.cfg")


while(app == None):
    pass  # Do nothing in particular while app is loading


app.Start()

time.sleep(5)

print(app.GetSignalValue(LAUNCH['bus_type'], int(LAUNCH['channel_num']), LAUNCH['msg_name'],
                       LAUNCH['sig_name']))'''


accel = 10
l = []
curr_speed = 251
target_speed = 1

moves = ceil(abs(target_speed-curr_speed)/accel)

if target_speed < curr_speed:
    if abs(target_speed-curr_speed) % accel != 0:
        for i in range(moves-1):
            curr_speed -= accel*1
            l.append(curr_speed)
            # time.sleep(1)

        curr_speed -= (abs(target_speed-curr_speed) % accel)

        l.append(curr_speed)
        print(l)
    else:
        for i in range(moves):
            curr_speed -= accel*1
            l.append(curr_speed)
        print(l)
else:
    if abs(target_speed-curr_speed) % accel != 0:
        for i in range(moves-1):
            curr_speed += accel*1
            l.append(curr_speed)
            # time.sleep(1)

        curr_speed += ((target_speed-curr_speed) % accel)

        l.append(curr_speed)
        print(l)
    else:
        for i in range(moves):
            curr_speed += accel*1
            l.append(curr_speed)
        print(l)