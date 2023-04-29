import helper
import CANoe
import ast
from math import ceil
from riden import Riden  # https://github.com/ShayBox/Riden
import time

# Parameters

# These are the default values for port, baudrate, and address
r = Riden(port="COM3", baudrate=115200, address=1)

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
# else:
#    app.Stop()
#    app.Load(
#        r"\Projects\Spoiler\CANoe_Simulation_SX_420\01_Configuration\HCP4_v13_DynTrace_PrivateCAN_BAP_GR.cfg")

while(app == None):
    pass  # Do nothing in particular while app is loading

app.Start()

time.sleep(10)


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


'''r.set_output(False)
time.sleep(1)
r.set_output(True)
time.sleep(1)'''


def test_601():
    # Clamp 15 is turned off and on again.

    STD_PRECONDITION()

    time.sleep(1)

    x = input('Press Enter if CLAMP15 is OFF: ')
    assert x == "", "Test Failed check CLAMP15"
    time.sleep(5)
    y = input('Press Enter if CLAMP15 is ON: ')
    assert y == "", "Test Failed check CLAMP15"
    time.sleep(5)

    AERO_SETUP_Value = helper.waitforsignal(
        app, AERO_SETUP, 17, deviation=100, timeout=10)

    assert 0 <= AERO_SETUP_Value <= 34, " AERO_SETUP position Failed, AERO SETUP Value = " + \
        str(AERO_SETUP_Value)


def test_602():
    # Clamp 30 is turned off and on again.

    STD_PRECONDITION()

    time.sleep(1)

    r.set_output(False)
    time.sleep(5)
    r.set_output(False)
    time.sleep(10)

    AERO_SETUP_Value = helper.waitforsignal(
        app, AERO_SETUP, 17, deviation=100, timeout=10)

    assert 0 <= AERO_SETUP_Value <= 34, " AERO_SETUP position Failed, AERO SETUP Value = " + \
        str(AERO_SETUP_Value)


def test_603():
    # Startup clamp 15 on, from manual mode

    STD_PRECONDITION()
    
    # BAP_START_SPOILER
    # BAP_Spoiler.SpoilerActuation = 1 for 200 ms

    time.sleep(1)

    AERO_SETUP_Value = helper.waitforsignal(
        app, AERO_SETUP, 36.5, deviation=100, timeout=10)

    assert 35 <= AERO_SETUP_Value <= 38, " AERO_SETUP position Failed, AERO SETUP Value = " + \
        str(AERO_SETUP_Value)

    x = input('Press Enter if CLAMP15 is OFF: ')
    assert x == "", "Test Failed check CLAMP15"
    time.sleep(5)
    y = input('Press Enter if CLAMP15 is ON: ')
    assert y == "", "Test Failed check CLAMP15"
    time.sleep(5)

    AERO_SETUP_Value = helper.waitforsignal(
        app, AERO_SETUP, 17, deviation=100, timeout=10)

    assert 0 <= AERO_SETUP_Value <= 34, " AERO_SETUP position Failed, AERO SETUP Value = " + \
        str(AERO_SETUP_Value)


def test_604():
    # Startup clamp 30 on, from manual mode

    STD_PRECONDITION()

    
    # BAP_START_SPOILER
    # BAP_Spoiler.SpoilerActuation = 1 for 200 ms

    time.sleep(1)

    AERO_SETUP_Value = helper.waitforsignal(
        app, AERO_SETUP, 36.5, deviation=100, timeout=10)

    assert 35 <= AERO_SETUP_Value <= 38, " AERO_SETUP position Failed, AERO SETUP Value = " + \
        str(AERO_SETUP_Value)

    r.set_output(False)
    time.sleep(5)
    r.set_output(False)
    time.sleep(10)

    AERO_SETUP_Value = helper.waitforsignal(
        app, AERO_SETUP, 17, deviation=100, timeout=10)

    assert 0 <= AERO_SETUP_Value <= 34, " AERO_SETUP position Failed, AERO SETUP Value = " + \
        str(AERO_SETUP_Value)


def test_605():
    # Finish movement with speed < v_TippTast

    STD_PRECONDITION()

    
    # BAP_START_SPOILER
    

    time.sleep(1)
    

def test_606():
    # Finish movement on clamp15 off

    STD_PRECONDITION()    

    time.sleep(1)
    
    helper.speedramp(app, ACTUAL_SPEED, vthresh_normal_ecotoperfo/3.6, accel=5)
    
    time.sleep(1)

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, PERFO_POS, deviation=10, timeout=10)

    assert PERFO_POS - Tolerance < spoilerpos < PERFO_POS + \
        Tolerance, "1Zero to Perfo position Failed, spoilerpos = " + \
        str(spoilerpos)
        
    helper.speedramp(app, ACTUAL_SPEED, vthresh_normal_min_move/3.6, accel=5)
    
    time.sleep(0.1)
    
    x = input('Press Enter if CLAMP15 is OFF: ')
    assert x == "", "Test Failed check CLAMP15"

    spoilerpos = helper.waitforsignal(
        app, ACTUAL_POS, ZERO_POS, deviation=10, timeout=10)

    assert ZERO_POS - Tolerance < spoilerpos < ZERO_POS + \
        Tolerance, "2Perfo to Zero position Failed, spoilerpos = " + \
        str(spoilerpos)