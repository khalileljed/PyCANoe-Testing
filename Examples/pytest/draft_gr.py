# import win32com.client
# import win32com.client.connect
from math import ceil
import time
import ast

import CANoe
import helper

# Parameters
config = helper.read_config()

# Spoiler Position
ZERO_POS = float(config['spoiler positions']['zero_pos'])
ECO_POS = float(config['spoiler positions']['eco_pos'])
PERFO_POS = float(config['spoiler positions']['perfo_pos'])
Tolerance = float(config['spoiler positions']['tolerance'])

# Drivemodes
DM_normal = int(config['Drivemodes']['dm_normal'])
DM_sport = int(config['Drivemodes']['dm_sport'])
DM_sportplus = int(config['Drivemodes']['dm_sportplus'])
DM_offroad = int(config['Drivemodes']['dm_offroad'])

# Signals
AERO_SETUP = ast.literal_eval(config['Signals']['aero_setup'])
ACTUAL_POS = ast.literal_eval(config['Signals']['actual_pos'])
ACTUAL_SPEED = ast.literal_eval(config['Signals']['actual_speed'])
LAUNCH = ast.literal_eval(config['Signals']['launch'])
DriveMode = ast.literal_eval(config['Signals']['drivemode'])
AERO_1_ERROR = ast.literal_eval(config['Signals']['aero_1_error'])
SUNROOF_POS = ast.literal_eval(config['Signals']['sunroof_pos'])
SUNROOF_LAGE = ast.literal_eval(config['Signals']['sunroof_lage'])

# Launchcontrol values
launch_init = int(config['Launchcontrol values']['launch_init'])
launch_prep = int(config['Launchcontrol values']['launch_prep'])
launch_active = int(config['Launchcontrol values']['launch_active'])
vthresh_launch_xtoeco = float(
    config['Launchcontrol values']['vthresh_launch_xtoeco'])
vthresh_launch_ecotoperfo = float(
    config['Launchcontrol values']['vthresh_launch_ecotoperfo'])

# Speed thresholds normal
vthresh_normal_min_move = float(
    config['Speed thresholds normal']['vthresh_normal_min_move'])
vthresh_normal_0toeco = float(
    config['Speed thresholds normal']['vthresh_normal_0toeco'])
vthresh_normal_ecoto0 = float(
    config['Speed thresholds normal']['vthresh_normal_ecoto0'])
vthresh_normal_ecotoperfo = float(
    config['Speed thresholds normal']['vthresh_normal_ecotoperfo'])
vthresh_normal_perfotoeco = float(
    config['Speed thresholds normal']['vthresh_normal_perfotoeco'])

# Speed thresholds sport
vthresh_sport_min_move = float(
    config['Speed thresholds sport']['vthresh_sport_min_move'])
vthresh_sport_0toeco = float(
    config['Speed thresholds sport']['vthresh_sport_0toeco'])
vthresh_sport_ecoto0 = float(
    config['Speed thresholds sport']['vthresh_sport_ecoto0'])
vthresh_sport_ecotoperfo = float(
    config['Speed thresholds sport']['vthresh_sport_ecotoperfo'])
vthresh_sport_perfotoeco = float(
    config['Speed thresholds sport']['vthresh_sport_perfotoeco'])

# Speed thresholds offroad
vthresh_offroad_min_move = float(
    config['Speed thresholds offroad']['vthresh_offroad_min_move'])
vthresh_offroad_0toeco = float(
    config['Speed thresholds offroad']['vthresh_offroad_0toeco'])
vthresh_offroad_ecoto0 = float(
    config['Speed thresholds offroad']['vthresh_offroad_ecoto0'])
vthresh_offroad_ecotoperfo = float(
    config['Speed thresholds offroad']['vthresh_offroad_ecotoperfo'])
vthresh_offroad_perfotoeco = float(
    config['Speed thresholds offroad']['vthresh_offroad_perfotoeco'])

# Speed thresholds sportplus
vthresh_splus_min_move = float(
    config['Speed thresholds sportplus']['vthresh_splus_min_move'])
vthresh_splus_0toeco = float(
    config['Speed thresholds sportplus']['vthresh_splus_0toeco'])
vthresh_splus_ecoto0 = float(
    config['Speed thresholds sportplus']['vthresh_splus_ecoto0'])
vthresh_splus_ecotoperfo = float(
    config['Speed thresholds sportplus']['vthresh_splus_ecotoperfo'])
vthresh_splus_perfotoeco = float(
    config['Speed thresholds sportplus']['vthresh_splus_perfotoeco'])

# Speed thresholds individual
vthresh_ind_min_move = float(
    config['Speed thresholds individual']['vthresh_ind_min_move'])
vthresh_ind_0toeco = float(
    config['Speed thresholds individual']['vthresh_ind_0toeco'])
vthresh_ind_ecoto0 = float(
    config['Speed thresholds individual']['vthresh_ind_ecoto0'])
vthresh_ind_ecotoperfo = float(
    config['Speed thresholds individual']['vthresh_ind_ecotoperfo'])
vthresh_ind_perfotoeco = float(
    config['Speed thresholds individual']['vthresh_ind_perfotoeco'])

# Speed thresholds manual
vthresh_manual_min_move = float(
    config['Speed thresholds manual']['vthresh_manual_min_move'])
vthresh_manual_0toeco = float(
    config['Speed thresholds manual']['vthresh_manual_0toeco'])
vthresh_manual_ecoto0 = float(
    config['Speed thresholds manual']['vthresh_manual_ecoto0'])
vthresh_manual_ecotoperfo = float(
    config['Speed thresholds manual']['vthresh_manual_ecotoperfo'])
vthresh_manual_perfotoeco = float(
    config['Speed thresholds manual']['vthresh_manual_perfotoeco'])

# SAD
vthresh_sad_xtoperfo = float(config['SAD']['vthresh_sad_xtoperfo'])
vthresh_sad_perfotox = float(config['SAD']['vthresh_sad_perfotox'])
vmax = float(config['SAD']['vmax'])

app = CANoe.CanoeSync()

if app == None:
    app.Load(
        r"\Projects\Spoiler\CANoe_Simulation_SX_420\01_Configuration\HCP4_v13_DynTrace_PrivateCAN_BAP_GR.cfg")
#else:
#    app.Stop()
#    app.Load(
#        r"\Projects\Spoiler\CANoe_Simulation_SX_420\01_Configuration\HCP4_v13_DynTrace_PrivateCAN_BAP_GR.cfg")

while(app == None):
    pass  # Do nothing in particular while app is loading

app.Start()

time.sleep(5)

spoilerpos = app.GetSignalValue("LIN", 7, "SP_01s_01", "SA1_Ist_Pos")
print(spoilerpos)

# print(app.GetEnvvarValue("ON_OFF_ASG64_1"))
# app.SetEnvvarValue("ON_OFF_ASG64_1",0)
# print(app.GetEnvvarValue("ON_OFF_ASG64_1"))
# app.SetEnvvarValue("ON_OFF_ASG64_1",1)
# print(app.GetEnvvarValue("ON_OFF_ASG64_1"))

helper.BAP_START_SPOILER(app)
time.sleep(1)

app.SetSysvarValue("AeroFkt::HMI", "SpoilerActuation_Actuation", 1)

time.sleep(3)
app.SetSysvarValue("AeroFkt::HMI", "SpoilerActuation_Actuation", 0)

# app.Stop()
