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

time.sleep(10)

'''
def waitforsignal(app, bus_type, channel_num, msg_name, sig_name, value, deviation=10, timeout=10):
    # Waits for a signal to reach value. accepted deviation from value in percent.
    # Fail after timeout. Standard values for deviation is 0 and for timeout is 10 seconds.
    i = 0
    while True:
        SigValue = app.GetSignalValue(
            bus_type, channel_num, msg_name, sig_name)
        i += 1
        time.sleep(1)
        # Here we make the check if the signal reached the value or we have timeout to stop execution.
        if value*(1-(deviation/100)) <= SigValue <= value*(1+(deviation/100)) or i == timeout:
            break
    return SigValue


def speedramp(app, bus_type, channel_num, msg_name, sig_name, target_speed, accel=5):
    # Gets current speed value and ramps it up/down with accel m/s² . Default accel is 5 m/s².
    curr_speed = app.GetSignalValue(bus_type, channel_num, msg_name, sig_name)

    moves = ceil((target_speed-curr_speed)/accel)
    for i in range(moves-1):
        curr_speed += accel*1  # time = 1 sec
        app.SetSignalValue(bus_type, channel_num,
                           msg_name, sig_name, curr_speed)
        time.sleep(1)
    curr_speed += ((target_speed-curr_speed) % accel)
    app.SetSignalValue(bus_type, channel_num, msg_name, sig_name, curr_speed)
'''


def STD_PRECONDITION():
    # Set SimulationControl to "send all messages" (Restbus Main Panel)
    app.SetSysvarValue("SimulationControl", "sv_SimulationControl", 1)

    time.sleep(1)

    # Precondition

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_normal)

    time.sleep(1)

    app.SetSignalValue(LAUNCH['bus_type'], int(LAUNCH['channel_num']), LAUNCH['msg_name'],
                       LAUNCH['sig_name'], launch_init)

    time.sleep(5)
    # SUNROOF_POS
    app.SetSignalValue(SUNROOF_POS['bus_type'], int(SUNROOF_POS['channel_num']), SUNROOF_POS['msg_name'],
                       SUNROOF_POS['sig_name'], 0)

    time.sleep(5)

    # SUNROOF_LAGE
    app.SetSignalValue(SUNROOF_LAGE['bus_type'], int(SUNROOF_LAGE['channel_num']), SUNROOF_LAGE['msg_name'],
                       SUNROOF_LAGE['sig_name'], 0)

    time.sleep(5)

    # allow spoiler to move to zero_pos by setting speed = 9 ACTUAL_SPEED
    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], 9)

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], 0)

    #spoilerpos = app.GetSignalValue("LIN", 7, "SP_01s_01", "SA1_Ist_Pos")

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ZERO_POS, deviation=10, timeout=10)

    assert ZERO_POS - Tolerance < spoilerpos < ZERO_POS + \
        Tolerance, "Precondition Failed, spoilerpos = " + str(spoilerpos)


def test_101():
    # Drive Mode DM_normal

    STD_PRECONDITION()

    time.sleep(1)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_normal_0toeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ECO_POS, deviation=10, timeout=10)

    assert ECO_POS - Tolerance < spoilerpos < ECO_POS + \
        Tolerance, "1Zero to Eco position Failed, spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_normal_ecotoperfo / 3.6)

    time.sleep(5)

    #spoilerpos = app.GetSignalValue("LIN", 7, "SP_01s_01", "SA1_Ist_Pos")

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, PERFO_POS, deviation=10, timeout=10)

    assert PERFO_POS - Tolerance < spoilerpos < PERFO_POS + \
        Tolerance, "2Eco to Perfo position Failed, spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_normal_perfotoeco / 3.6)

    time.sleep(5)

    #spoilerpos = app.GetSignalValue("LIN", 7, "SP_01s_01", "SA1_Ist_Pos")

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ECO_POS, deviation=10, timeout=10)

    assert ECO_POS - Tolerance < spoilerpos < ECO_POS + \
        Tolerance, "3Perfo to Eco position Failed, spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_normal_ecoto0 / 3.6)

    time.sleep(5)

    #spoilerpos = app.GetSignalValue("LIN", 7, "SP_01s_01", "SA1_Ist_Pos")

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ZERO_POS, deviation=10, timeout=10)

    assert ZERO_POS - Tolerance < spoilerpos < ZERO_POS + \
        Tolerance, "4Eco to Zero position Failed, spoilerpos = " + \
        str(spoilerpos)


def test_102():
    # Drive Mode DM_sport

    STD_PRECONDITION()
    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sport)

    time.sleep(1)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_sport_0toeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ECO_POS, deviation=10, timeout=10)

    assert ECO_POS - Tolerance < spoilerpos < ECO_POS + \
        Tolerance, "Zero to Eco position Failed"

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_sport_ecotoperfo / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, PERFO_POS, deviation=10, timeout=10)

    assert PERFO_POS - Tolerance < spoilerpos < PERFO_POS + \
        Tolerance, "Eco to Perfo position Failed"

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_sport_perfotoeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ECO_POS, deviation=10, timeout=10)

    assert ECO_POS - Tolerance < spoilerpos < ECO_POS + \
        Tolerance, "Perfo to Eco position Failed"

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_sport_ecoto0 / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ZERO_POS, deviation=10, timeout=10)

    assert ZERO_POS - Tolerance < spoilerpos < ZERO_POS + \
        Tolerance, "Eco to Zero position Failed"


def test_103():
    # Drive Mode DM_sportplus
    STD_PRECONDITION()
    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sportplus)

    time.sleep(1)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_splus_0toeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ECO_POS, deviation=10, timeout=10)

    assert ECO_POS - Tolerance < spoilerpos < ECO_POS + \
        Tolerance, "Zero to Eco position Failed"

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_splus_ecotoperfo / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, PERFO_POS, deviation=10, timeout=10)

    assert PERFO_POS - Tolerance < spoilerpos < PERFO_POS + \
        Tolerance, "Eco to Perfo position Failed"

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_splus_perfotoeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ECO_POS, deviation=10, timeout=10)

    assert ECO_POS - Tolerance < spoilerpos < ECO_POS + \
        Tolerance, "Perfo to Eco position Failed"

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_splus_ecoto0 / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ZERO_POS, deviation=10, timeout=10)

    assert ZERO_POS - Tolerance < spoilerpos < ZERO_POS + \
        Tolerance, "Eco to Zero position Failed"


def test_104():
    # Switch Drive Mode from DM_normal to DM_sportplus
    STD_PRECONDITION()

    time.sleep(1)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_normal_0toeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ECO_POS, deviation=10, timeout=10)

    assert ECO_POS - Tolerance < spoilerpos < ECO_POS + \
        Tolerance, "Zero to Eco position Failed, DM_normal , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_splus_ecotoperfo / 3.6)

    time.sleep(5)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sportplus)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, PERFO_POS, deviation=10, timeout=10)

    assert PERFO_POS - Tolerance < spoilerpos < PERFO_POS + \
        Tolerance, "Eco to Perfo position Failed, DM_sportplus , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_splus_perfotoeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ECO_POS, deviation=10, timeout=10)

    assert ECO_POS - Tolerance < spoilerpos < ECO_POS + \
        Tolerance, "Perfo to Eco position Failed, DM_sportplus , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_splus_ecoto0 / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ZERO_POS, deviation=10, timeout=10)

    assert ZERO_POS - Tolerance < spoilerpos < ZERO_POS + \
        Tolerance, "Eco to Zero position Failed, DM_sportplus , spoilerpos = " + \
        str(spoilerpos)


def test_105():
    # Switch Drive Mode from DM_sportplus to DM_normal
    STD_PRECONDITION()
    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sportplus)

    time.sleep(1)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_splus_0toeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ECO_POS, deviation=10, timeout=10)

    assert ECO_POS - Tolerance < spoilerpos < ECO_POS + \
        Tolerance, "Zero to Eco position Failed, DM_sportplus , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_splus_ecotoperfo / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, PERFO_POS, deviation=10, timeout=10)

    assert PERFO_POS - Tolerance < spoilerpos < PERFO_POS + \
        Tolerance, "Eco to Perfo Failed, DM_sportplus , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_normal)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ECO_POS, deviation=10, timeout=10)

    assert ECO_POS - Tolerance < spoilerpos < ECO_POS + \
        Tolerance, "Perfo to Eco Failed, DM_normal , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_normal_ecotoperfo / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, PERFO_POS, deviation=10, timeout=10)

    assert PERFO_POS - Tolerance < spoilerpos < PERFO_POS + \
        Tolerance, "Eco to Perfo Failed, DM_normal , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_normal_perfotoeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ECO_POS, deviation=10, timeout=10)

    assert ECO_POS - Tolerance < spoilerpos < ECO_POS + \
        Tolerance, "Perfo to Eco position Failed, DM_normal , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_normal_ecoto0 / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ZERO_POS, deviation=10, timeout=10)

    assert ZERO_POS - Tolerance < spoilerpos < ZERO_POS + \
        Tolerance, "Eco to Zero position Failed, DM_normal , spoilerpos = " + \
        str(spoilerpos)


def test_106():
    # Switch Drive Mode from DM_sport to DM_sportplus
    STD_PRECONDITION()

    time.sleep(1)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sport)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_sport_0toeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ECO_POS, deviation=10, timeout=10)

    assert ECO_POS - Tolerance < spoilerpos < ECO_POS + \
        Tolerance, "Zero to Eco position Failed, DM_normal , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_splus_ecotoperfo / 3.6)

    time.sleep(5)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sportplus)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, PERFO_POS, deviation=10, timeout=10)

    assert PERFO_POS - Tolerance < spoilerpos < PERFO_POS + \
        Tolerance, "Eco to Perfo position Failed, DM_sportplus , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_splus_perfotoeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, PERFO_POS, deviation=10, timeout=10)

    assert ECO_POS - Tolerance < spoilerpos < ECO_POS + \
        Tolerance, "Perfo to Eco position Failed, DM_sportplus , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_splus_ecoto0 / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ZERO_POS, deviation=10, timeout=10)

    assert ZERO_POS - Tolerance < spoilerpos < ZERO_POS + \
        Tolerance, "Eco to Zero position Failed, DM_sportplus , spoilerpos = " + \
        str(spoilerpos)


def test_107():
    # Switch Drive Mode from DM_sportplus to DM_sport
    STD_PRECONDITION()
    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sportplus)

    time.sleep(1)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_splus_0toeco / 3.6)

    time.sleep(5)

    #spoilerpos = app.GetSignalValue("LIN", 7, "SP_01s_01", "SA1_Ist_Pos")

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ECO_POS, deviation=10, timeout=10)

    assert ECO_POS - Tolerance < spoilerpos < ECO_POS + \
        Tolerance, "Zero to Eco position Failed, DM_sportplus , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_splus_ecotoperfo / 3.6)

    time.sleep(5)

    #spoilerpos = app.GetSignalValue("LIN", 7, "SP_01s_01", "SA1_Ist_Pos")

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, PERFO_POS, deviation=10, timeout=10)

    assert PERFO_POS - Tolerance < spoilerpos < PERFO_POS + \
        Tolerance, "Eco to Perfo Failed, DM_sportplus , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sport)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ECO_POS, deviation=10, timeout=10)

    assert ECO_POS - Tolerance < spoilerpos < ECO_POS + \
        Tolerance, "Perfo to Eco Failed, DM_normal , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_sport_ecotoperfo / 3.6)

    time.sleep(5)

    #spoilerpos = app.GetSignalValue("LIN", 7, "SP_01s_01", "SA1_Ist_Pos")

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, PERFO_POS, deviation=10, timeout=10)

    assert PERFO_POS - Tolerance < spoilerpos < PERFO_POS + \
        Tolerance, "Eco to Perfo Failed, DM_normal , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_sport_perfotoeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ECO_POS, deviation=10, timeout=10)

    assert ECO_POS - Tolerance < spoilerpos < ECO_POS + \
        Tolerance, "Perfo to Eco position Failed, DM_normal , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], vthresh_sport_ecoto0 / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ZERO_POS, deviation=10, timeout=10)

    assert ZERO_POS - Tolerance < spoilerpos < ZERO_POS + \
        Tolerance, "Eco to Zero position Failed, DM_normal , spoilerpos = " + \
        str(spoilerpos)


def test_108():
    # "Change driving mode with speed > vMaxFahrProg

    STD_PRECONDITION()

    time.sleep(1)

    app.SetSignalValue(ACTUAL_SPEED['bus_type'], int(ACTUAL_SPEED['channel_num']), ACTUAL_SPEED['msg_name'],
                       ACTUAL_SPEED['sig_name'], (vmax-1) / 3.6)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, PERFO_POS, deviation=10, timeout=10)

    assert PERFO_POS - Tolerance < spoilerpos < PERFO_POS + \
        Tolerance, "1Zero to Perfo position Failed, spoilerpos = " + \
        str(spoilerpos)

    time.sleep(1)

    AERO_SETUP_Value = helper.waitforsignal(
        app, AERO_SETUP, 3, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 3, " 1AERO_SETUP position Failed, AERO SETUP Value = " + \
        str(AERO_SETUP_Value)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sportplus)

    time.sleep(1)

    AERO_SETUP_Value = helper.waitforsignal(
        app, AERO_SETUP, 13, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 13, " 2AERO_SETUP position Failed, AERO SETUP Value = " + \
        str(AERO_SETUP_Value)


def test_109():
    # Fast braking

    STD_PRECONDITION()

    time.sleep(1)

    #app.SetSignalValue("Ethernet", 1, "VDSO_01_XIX_VLAN_Komfort","VDSO_Vx6d_XIX_VDSO_01_XIX_VLAN_Komfort", 250/3.6)

    helper.speedramp(app, ACTUAL_SPEED, vmax/3.6, accel=5)
    time.sleep(1)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, PERFO_POS, deviation=10, timeout=10)

    assert PERFO_POS - Tolerance < spoilerpos < PERFO_POS + \
        Tolerance, "1Zero to Perfo position Failed, spoilerpos = " + \
        str(spoilerpos)

    helper.speedramp(app, ACTUAL_SPEED, 0, 10)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ZERO_POS, deviation=10, timeout=10)

    assert ZERO_POS - Tolerance < spoilerpos < ZERO_POS + \
        Tolerance, "2Perfo to Zero position Failed, spoilerpos = " + \
        str(spoilerpos)


def test_110():
    # Quick cycle of driving modes, end in same mode

    STD_PRECONDITION()

    time.sleep(1)

    helper.speedramp(app, ACTUAL_SPEED, 100/3.6, accel=5)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ECO_POS, deviation=10, timeout=10)

    assert ECO_POS - Tolerance < spoilerpos < ECO_POS + \
        Tolerance, "1Zero to Eco position Failed, spoilerpos = " + \
        str(spoilerpos)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sport)

    time.sleep(0.1)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sportplus)

    time.sleep(0.1)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_offroad)

    time.sleep(0.1)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_normal)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ECO_POS, deviation=10, timeout=10)

    assert ECO_POS - Tolerance < spoilerpos < ECO_POS + \
        Tolerance, "2Eco position Failed, spoilerpos = " + \
        str(spoilerpos)


def test_111():
    # Quick cycle of driving modes, end in different mode

    STD_PRECONDITION()

    time.sleep(1)

    helper.speedramp(app, ACTUAL_SPEED, 100/3.6, accel=5)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ECO_POS, deviation=10, timeout=10)

    assert ECO_POS - Tolerance < spoilerpos < ECO_POS + \
        Tolerance, "1Zero to Eco position Failed, spoilerpos = " + \
        str(spoilerpos)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sport)

    time.sleep(0.1)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sportplus)

    time.sleep(0.1)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_offroad)

    time.sleep(0.1)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_normal)

    time.sleep(0.1)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sportplus)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, PERFO_POS, deviation=10, timeout=10)

    assert PERFO_POS - Tolerance < spoilerpos < PERFO_POS + \
        Tolerance, "2Eco to Perfo position Failed, spoilerpos = " + \
        str(spoilerpos)


def test_112():
    # Quick cycle of driving modes, end in same mode - standing still

    STD_PRECONDITION()

    time.sleep(1)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sport)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ZERO_POS, deviation=10, timeout=10)

    assert ZERO_POS - Tolerance < spoilerpos < ZERO_POS + \
        Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    time.sleep(0.1)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sport)

    time.sleep(0.1)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sportplus)

    time.sleep(0.1)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_offroad)

    time.sleep(0.1)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_normal)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ZERO_POS, deviation=10, timeout=10)

    assert ZERO_POS - Tolerance < spoilerpos < ZERO_POS + \
        Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    AERO_1_ERROR_VALUE = helper.waitforsignal(
        app, AERO_1_ERROR, 0, deviation=10, timeout=10)

    assert AERO_1_ERROR_VALUE == 0


def test_113():
    # Quick cycle of driving modes, end in different mode - standing still

    STD_PRECONDITION()

    time.sleep(1)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sport)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ZERO_POS, deviation=10, timeout=10)

    assert ZERO_POS - Tolerance < spoilerpos < ZERO_POS + \
        Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    time.sleep(0.1)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sport)

    time.sleep(0.1)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sportplus)

    time.sleep(0.1)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_offroad)

    time.sleep(0.1)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_normal)

    time.sleep(0.1)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sportplus)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ZERO_POS, deviation=10, timeout=10)

    assert ZERO_POS - Tolerance < spoilerpos < ZERO_POS + \
        Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    AERO_1_ERROR_VALUE = helper.waitforsignal(
        app, AERO_1_ERROR, 0, deviation=10, timeout=10)

    assert AERO_1_ERROR_VALUE == 0


def test_114():
    # Slow cycle of driving modes, standing

    STD_PRECONDITION()

    time.sleep(1)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sport)

    time.sleep(2)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ZERO_POS, deviation=10, timeout=10)

    assert ZERO_POS - Tolerance < spoilerpos < ZERO_POS + \
        Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sport)

    time.sleep(2)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ZERO_POS, deviation=10, timeout=10)

    assert ZERO_POS - Tolerance < spoilerpos < ZERO_POS + \
        Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sportplus)

    time.sleep(2)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ZERO_POS, deviation=10, timeout=10)

    assert ZERO_POS - Tolerance < spoilerpos < ZERO_POS + \
        Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_offroad)

    time.sleep(2)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ZERO_POS, deviation=10, timeout=10)

    assert ZERO_POS - Tolerance < spoilerpos < ZERO_POS + \
        Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_normal)

    time.sleep(2)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ZERO_POS, deviation=10, timeout=10)

    assert ZERO_POS - Tolerance < spoilerpos < ZERO_POS + \
        Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sport)

    time.sleep(2)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ZERO_POS, deviation=10, timeout=10)

    assert ZERO_POS - Tolerance < spoilerpos < ZERO_POS + \
        Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_sportplus)

    time.sleep(2)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ZERO_POS, deviation=10, timeout=10)

    assert ZERO_POS - Tolerance < spoilerpos < ZERO_POS + \
        Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    app.SetSignalValue(DriveMode['bus_type'], int(DriveMode['channel_num']), DriveMode['msg_name'],
                       DriveMode['sig_name'], DM_offroad)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ZERO_POS, deviation=10, timeout=10)

    assert ZERO_POS - Tolerance < spoilerpos < ZERO_POS + \
        Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    AERO_1_ERROR_VALUE = helper.waitforsignal(
        app, AERO_1_ERROR, 0, deviation=10, timeout=10)

    assert AERO_1_ERROR_VALUE == 0

# app.Stop()
