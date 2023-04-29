from math import ceil
import time
import ast
import CANoe
import helper
from riden import Riden  # pip install --user git+https://github.com/shaybox/riden.git
import parameters as P

# These are the default values for port, baudrate, and address
r = helper.Riden_Connect()

app = CANoe.CanoeSync()

if app == None:
    app.Load(
        r"\Projects\Spoiler\CANoe_Simulation_SX_420\01_Configuration\HCP4_v13_DynTrace_PrivateCAN_BAP_GR.cfg")
# else:
#     app.Stop()
#     app.Load(
#         r"\Projects\Spoiler\CANoe_Simulation_SX_420\01_Configuration\HCP4_v13_DynTrace_PrivateCAN_BAP_GR.cfg")

while (app == None):
    pass  # Do nothing in particular while app is loading

app.Start()

time.sleep(5)


def test_201_NoUser():
    # "DM_normal:Init Launchcontrol and hold till 200 km/h. Decelerate to 0 km/h."

    helper.STD_PRECONDITION(app, r)

    app.SetSignalValue(P.LAUNCH['bus_type'], int(P.LAUNCH['channel_num']), P.LAUNCH['msg_name'],
                       P.LAUNCH['sig_name'], P.launch_active)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
           P.Tolerance, "1Zero to Eco position Failed, spoilerpos = " + \
                        str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, 48, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 48, " 1AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    time.sleep(2)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     (P.vthresh_launch_ecotoperfo - 2) / 3.6, accel=5, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
           P.Tolerance, "2Eco position Failed, spoilerpos = " + str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, 48, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 48, " 2AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    time.sleep(2)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.vthresh_launch_ecotoperfo / 3.6, accel=5, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
           P.Tolerance, "3Eco to Perfo position Failed, spoilerpos = " + \
                        str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 49, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 49, " 3AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    time.sleep(2)

    helper.speedramp(app, P.ACTUAL_SPEED, 200 / 3.6, accel=5, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
           P.Tolerance, "4Perfo Position Failed, spoilerpos = " + str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 49, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 49, " 4AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    time.sleep(1)

    app.SetSignalValue(P.LAUNCH['bus_type'], int(P.LAUNCH['channel_num']), P.LAUNCH['msg_name'],
                       P.LAUNCH['sig_name'], P.launch_init)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.vthresh_normal_min_move / 3.6, accel=5, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
           P.Tolerance, "5Perfo Position Failed, spoilerpos = " + str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 0, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 0, " 5AERO_SETUP Failed, AERO SETUP Value = " + \
                                  str(AERO_SETUP_Value)


def test_202_NoUser():
    # "P.DM_sport:Init Launchcontrol and hold till 200 km/h. Decelerate to 0 km/h."

    helper.STD_PRECONDITION(app, r)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sport)

    app.SetSignalValue(P.LAUNCH['bus_type'], int(P.LAUNCH['channel_num']), P.LAUNCH['msg_name'],
                       P.LAUNCH['sig_name'], P.launch_active)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
           P.Tolerance, "1Zero to Eco position Failed, spoilerpos = " + \
                        str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, 48, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 48, " 1AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    time.sleep(2)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     (P.vthresh_launch_ecotoperfo - 2) / 3.6, accel=5, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
           P.Tolerance, "2Eco position Failed, spoilerpos = " + str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, 48, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 48, " 2AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    time.sleep(2)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.vthresh_launch_ecotoperfo / 3.6, accel=5, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
           P.Tolerance, "3Eco to Perfo position Failed, spoilerpos = " + \
                        str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 49, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 49, "P.AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    time.sleep(2)

    helper.speedramp(app, P.ACTUAL_SPEED, 200 / 3.6, accel=5, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
           P.Tolerance, "4Perfo Position Failed, spoilerpos = " + str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 49, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 49, "P.AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    time.sleep(1)

    app.SetSignalValue(P.LAUNCH['bus_type'], int(P.LAUNCH['channel_num']), P.LAUNCH['msg_name'],
                       P.LAUNCH['sig_name'], P.launch_init)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.vthresh_sport_min_move / 3.6, accel=5, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
           P.Tolerance, "5Perfo Position Failed, spoilerpos = " + str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 0, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 5, "P.AERO_SETUP Failed, AERO SETUP Value = " + \
                                  str(AERO_SETUP_Value)


def test_203_NoUser():
    # "P.DM_sportplus:Init Launchcontrol and hold till 200 km/h. Decelerate to 0 km/h."

    helper.STD_PRECONDITION(app, r)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sportplus)

    app.SetSignalValue(P.LAUNCH['bus_type'], int(P.LAUNCH['channel_num']), P.LAUNCH['msg_name'],
                       P.LAUNCH['sig_name'], P.launch_active)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
           P.Tolerance, "1Zero to Eco position Failed, spoilerpos = " + \
                        str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, 48, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 48, " 1AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    time.sleep(2)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     (P.vthresh_launch_ecotoperfo - 2) / 3.6, accel=5, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
           P.Tolerance, "2Eco position Failed, spoilerpos = " + str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, 48, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 48, " 2AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    time.sleep(2)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.vthresh_launch_ecotoperfo / 3.6, accel=5, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
           P.Tolerance, "Eco to Perfo position Failed, spoilerpos = " + \
                        str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 49, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 49, "P.AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    time.sleep(2)

    helper.speedramp(app, P.ACTUAL_SPEED, 200 / 3.6, accel=5, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
           P.Tolerance, "Perfo Position Failed, spoilerpos = " + str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 49, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 49, "P.AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    time.sleep(1)

    app.SetSignalValue(P.LAUNCH['bus_type'], int(P.LAUNCH['channel_num']), P.LAUNCH['msg_name'],
                       P.LAUNCH['sig_name'], P.launch_init)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.vthresh_splus_min_move / 3.6, accel=5, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
           P.Tolerance, "Perfo Position Failed, spoilerpos = " + str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 0, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 10, "P.AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)


def test_204_NoUser():
    # "P.DM_offroad:Init Launchcontrol and hold till 200 km/h. Decelerate to 0 km/h."

    helper.STD_PRECONDITION(app, r)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_offroad)

    app.SetSignalValue(P.LAUNCH['bus_type'], int(P.LAUNCH['channel_num']), P.LAUNCH['msg_name'],
                       P.LAUNCH['sig_name'], P.launch_active)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
           P.Tolerance, "1Zero to Eco position Failed, spoilerpos = " + \
                        str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, 48, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 48, " 1AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    time.sleep(2)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     (P.vthresh_launch_ecotoperfo - 2) / 3.6, accel=5, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
           P.Tolerance, "2Eco position Failed, spoilerpos = " + str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, 48, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 48, " 2AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    time.sleep(2)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.vthresh_launch_ecotoperfo / 3.6, accel=5, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
           P.Tolerance, "3Eco to Perfo position Failed, spoilerpos = " + \
                        str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 49, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 49, " 3AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    time.sleep(2)

    helper.speedramp(app, P.ACTUAL_SPEED, 200 / 3.6, accel=5, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
           P.Tolerance, "4Perfo Position Failed, spoilerpos = " + str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 49, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 49, " 4AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    time.sleep(1)

    app.SetSignalValue(P.LAUNCH['bus_type'], int(P.LAUNCH['channel_num']), P.LAUNCH['msg_name'],
                       P.LAUNCH['sig_name'], P.launch_init)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.vthresh_offroad_min_move / 3.6, accel=5, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
           P.Tolerance, "5Perfo Position Failed, spoilerpos = " + str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 0, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 15, " 5AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)


def test_205_NoUser():
    # "DM_normal with SAD open Init Launchcontrol and hold till 200 km/h. Decelerate to 0 km/h."

    helper.STD_PRECONDITION(app, r)

    helper.SAD_OPEN(app)

    app.SetSignalValue(P.LAUNCH['bus_type'], int(P.LAUNCH['channel_num']), P.LAUNCH['msg_name'],
                       P.LAUNCH['sig_name'], P.launch_active)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
           P.Tolerance, "1Eco Position Failed, spoilerpos = " + str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, 48, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 48, " 1AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    time.sleep(2)

    helper.speedramp(app, P.ACTUAL_SPEED, P.vthresh_sad_xtoperfo / 3.6, accel=5, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
           P.Tolerance, "2Perfo Position Failed, spoilerpos = " + str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 40, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 40, " 2AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    time.sleep(2)

    helper.speedramp(app, P.ACTUAL_SPEED, 200 / 3.6, accel=5, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
           P.Tolerance, "3Perfo Position Failed, spoilerpos = " + str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 40, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 40, " 3AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    time.sleep(2)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.vthresh_normal_min_move / 3.6, accel=5, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
           P.Tolerance, "4Zero Position Failed, spoilerpos = " + str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 0, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 0, " 4AERO_SETUP Failed, AERO SETUP Value = " + \
                                  str(AERO_SETUP_Value)


def test_206_NoUser():
    # "DM_normal:Init Launchcontrol and hold till 54 km/h. Then drop Launchcontrol."

    helper.STD_PRECONDITION(app, r)

    app.SetSignalValue(P.LAUNCH['bus_type'], int(P.LAUNCH['channel_num']), P.LAUNCH['msg_name'],
                       P.LAUNCH['sig_name'], P.launch_active)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
           P.Tolerance, "1Zero to Eco position Failed, spoilerpos = " + \
                        str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, 48, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 48, " 1AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    time.sleep(5)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     (P.vthresh_normal_0toeco - 2) / 3.6, accel=5, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
           P.Tolerance, "2Eco position Failed, spoilerpos = " + str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, 48, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 48, " 2AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    time.sleep(5)

    app.SetSignalValue(P.LAUNCH['bus_type'], int(P.LAUNCH['channel_num']), P.LAUNCH['msg_name'],
                       P.LAUNCH['sig_name'], P.launch_init)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
           P.Tolerance, "3Eco to Zero position Failed, spoilerpos = " + \
                        str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 0, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 0, " 3AERO_SETUP Failed, AERO SETUP Value = " + \
                                  str(AERO_SETUP_Value)


def test_207_NoUser():
    # "P.DM_sport:Init Launchcontrol and hold till 54 km/h. Then drop Launchcontrol."

    helper.STD_PRECONDITION(app, r)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sport)

    app.SetSignalValue(P.LAUNCH['bus_type'], int(P.LAUNCH['channel_num']), P.LAUNCH['msg_name'],
                       P.LAUNCH['sig_name'], P.launch_active)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
           P.Tolerance, "1Zero to Eco position Failed, spoilerpos = " + \
                        str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, 48, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 48, " 1AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    time.sleep(5)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     (P.vthresh_sport_0toeco - 2) / 3.6, accel=5, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
           P.Tolerance, "2Eco position Failed, spoilerpos = " + str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, 48, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 48, " 2AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    time.sleep(5)

    app.SetSignalValue(P.LAUNCH['bus_type'], int(P.LAUNCH['channel_num']), P.LAUNCH['msg_name'],
                       P.LAUNCH['sig_name'], P.launch_init)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
           P.Tolerance, "3Eco to Zero position Failed, spoilerpos = " + \
                        str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 5, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 5, " 3AERO_SETUP Failed, AERO SETUP Value = " + \
                                  str(AERO_SETUP_Value)


def test_208_NoUser():
    # "P.DM_sportplus:Init Launchcontrol and hold till 90 km/h. Then drop Launchcontrol."

    helper.STD_PRECONDITION(app, r)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sportplus)

    app.SetSignalValue(P.LAUNCH['bus_type'], int(P.LAUNCH['channel_num']), P.LAUNCH['msg_name'],
                       P.LAUNCH['sig_name'], P.launch_active)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
           P.Tolerance, "1Zero to Eco position Failed, spoilerpos = " + \
                        str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 48, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 48, " 1AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    # time.sleep(5)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.vthresh_splus_ecotoperfo / 3.6, accel=5, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
           P.Tolerance, "Eco position Failed, spoilerpos = " + str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 48, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 48, "P.AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    # time.sleep(5)

    app.SetSignalValue(P.LAUNCH['bus_type'], int(P.LAUNCH['channel_num']), P.LAUNCH['msg_name'],
                       P.LAUNCH['sig_name'], P.launch_init)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
           P.Tolerance, "Eco to Perfo position Failed, spoilerpos = " + \
                        str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 12, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 12, "P.AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)


def test_209_NoUser():
    helper.STD_PRECONDITION(app, r)
    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.vthresh_normal_min_move / 3.6, accel=20, update_rate=10)

    app.SetSignalValue(P.LAUNCH['bus_type'], int(P.LAUNCH['channel_num']), P.LAUNCH['msg_name'],
                       P.LAUNCH['sig_name'], P.launch_active)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
           P.Tolerance, "1Eco Position Failed, spoilerpos = " + str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, 48, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 48, " 1AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    helper.BAP_TIPP(app)

    time.sleep(1)

    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, P.MAN_SETUP_1, deviation=0, timeout=10)

    assert AERO_SETUP_Value == P.MAN_SETUP_1, " 2AERO_SETUP Failed, AERO SETUP Value = " + \
                                              str(AERO_SETUP_Value)

    app.SetSignalValue(P.LAUNCH['bus_type'], int(P.LAUNCH['channel_num']), P.LAUNCH['msg_name'],
                       P.LAUNCH['sig_name'], P.launch_init)
    time.sleep(1)

    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, 0, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 0, " 3AERO_SETUP Failed, AERO SETUP Value = " + \
                                  str(AERO_SETUP_Value)

    app.SetSignalValue(P.LAUNCH['bus_type'], int(P.LAUNCH['channel_num']), P.LAUNCH['msg_name'],
                       P.LAUNCH['sig_name'], P.launch_init)

    time.sleep(2)

    spoilerpos = helper.waitforsignal(app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
           P.Tolerance, "2Eco Position Failed, spoilerpos = " + str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, P.MAN_SETUP_1, deviation=0, timeout=10)

    assert AERO_SETUP_Value == P.MAN_SETUP_1, " 4AERO_SETUP Failed, AERO SETUP Value = " + \
                                              str(AERO_SETUP_Value)


def test_210_NoUser():
    helper.STD_PRECONDITION(app, r)

    app.SetSignalValue(P.LAUNCH['bus_type'], int(P.LAUNCH['channel_num']), P.LAUNCH['msg_name'],
                       P.LAUNCH['sig_name'], P.launch_active)
    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.Vthresh_SAD_Setup0to1 / 3.6, accel=5, update_rate=10)

    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, 48, deviation=0, timeout=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
           P.Tolerance, "1Eco Position Failed, spoilerpos = " + str(spoilerpos)

    assert AERO_SETUP_Value == 48, " 1AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    app.SetSignalValue(P.SUNROOF_POS['bus_type'], int(P.SUNROOF_POS['channel_num']), P.SUNROOF_POS['msg_name'],
                       P.SUNROOF_POS['sig_name'], 120)
    app.SetSignalValue(P.SUNROOF_LAGE['bus_type'], int(P.SUNROOF_LAGE['channel_num']), P.SUNROOF_LAGE['msg_name'],
                       P.SUNROOF_LAGE['sig_name'], 1)

    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, 40, deviation=0, timeout=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
           P.Tolerance, "1Perfo Position Failed, spoilerpos = " + str(spoilerpos)

    assert AERO_SETUP_Value == 40, " 2AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)


def test_211_NoUser():
    helper.STD_PRECONDITION(app, r)

    app.SetSysvarValue("MessageControl::VLAN_Komfort::SimulatedPeerNode::HCP1_09_XIX_VLAN_Komfort",
                       "sv_HCP1_09_XIX_VLAN_Komfort", 0)
    time.sleep(5)

    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, 0, deviation=0, timeout=10)
    assert AERO_SETUP_Value == 0, " 1AERO_SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
           P.Tolerance, "1Zero position Failed, spoilerpos = " + \
                        str(spoilerpos)

