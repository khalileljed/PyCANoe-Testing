import helper
import CANoe
import ast
from math import ceil
from riden import Riden  # https://github.com/ShayBox/Riden
import time
import ctypes  # An included library with Python install.
import parameters as P
import pytest

# These are the default values for port, baudrate, and address
r = helper.Riden_Connect()

app = CANoe.CanoeSync()

if app == None:
    app.Load(
        r"\Projects\Spoiler\CANoe_Simulation_SX_420\01_Configuration\HCP4_v13_DynTrace_PrivateCAN_BAP_GR.cfg")
# else:
#    app.Stop()
#    app.Load(
#        r"\Projects\Spoiler\CANoe_Simulation_SX_420\01_Configuration\HCP4_v13_DynTrace_PrivateCAN_BAP_GR.cfg")

while (app == None):
    pass  # Do nothing in particular while app is loading

app.Start()

time.sleep(5)


def test_701_NoUser():
    helper.STD_PRECONDITION(app, r)

    helper.BAP_START_SPOILER(app)
    time.sleep(1)

    helper.BAP_TIPP(app)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, P.MAN_SETUP_1, deviation=0, timeout=10)

    assert AERO_SETUP_Value == P.MAN_SETUP_1, " 1AERO SETUP Failed, AERO SETUP Value = " + \
                                              str(AERO_SETUP_Value)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
           P.Tolerance, "1Eco position Failed, spoilerpos = " + \
                        str(spoilerpos)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.vthresh_man_setup1to2 / 3.6, accel=5, update_rate=10)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, P.MAN_SETUP_2, deviation=0, timeout=10)

    assert AERO_SETUP_Value == P.MAN_SETUP_2, " 2AERO SETUP Failed, AERO SETUP Value = " + \
                                              str(AERO_SETUP_Value)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
           P.Tolerance, "2Perfo position Failed, spoilerpos = " + \
                        str(spoilerpos)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.vthresh_man_setup2to3 / 3.6, accel=5, update_rate=10)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, P.MAN_SETUP_3, deviation=0, timeout=10)

    assert AERO_SETUP_Value == P.MAN_SETUP_3, " 3AERO SETUP Failed, AERO SETUP Value = " + \
                                              str(AERO_SETUP_Value)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
           P.Tolerance, "3Perfo position Failed, spoilerpos = " + \
                        str(spoilerpos)


def test_702_NoUser():
    helper.STD_PRECONDITION(app, r)

    helper.BAP_START_SPOILER(app)
    time.sleep(1)

    helper.BAP_TIPP(app)

    BAP_LED = app.GetEnvvarValue("P_ASG_64_1_0_18_1")
    assert BAP_LED == 1, "1Check BAP LED"
    time.sleep(1)
    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
           P.Tolerance, "1Eco position Failed, spoilerpos = " + \
                        str(spoilerpos)

    helper.BAP_TIPP(app)

    time.sleep(6)

    BAP_LED = app.GetEnvvarValue("P_ASG_64_1_0_18_1")
    assert BAP_LED == 3, "2Check BAP LED"

    helper.BAP_TIPP(app)

    BAP_LED = app.GetEnvvarValue("P_ASG_64_1_0_18_1")
    assert BAP_LED == 1, "3Check BAP LED"

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
           P.Tolerance, "2Eco position Failed, spoilerpos = " + \
                        str(spoilerpos)

    helper.BAP_TAST(app, 5)

    BAP_LED = app.GetEnvvarValue("P_ASG_64_1_0_18_1")
    assert BAP_LED == 0, "4Check BAP LED"

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
           P.Tolerance, "3Zero position Failed, spoilerpos = " + \
                        str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 0, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 0, " 1AERO SETUP Failed, AERO SETUP Value = " + \
                                  str(AERO_SETUP_Value)


def test_703_NoUser():
    helper.STD_PRECONDITION(app, r)

    helper.BAP_START_SPOILER(app)
    time.sleep(1)

    helper.BAP_TIPP(app)

    BAP_LED = app.GetEnvvarValue("P_ASG_64_1_0_18_1")
    assert BAP_LED == 1, "1Check BAP LED"

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
           P.Tolerance, "1Eco position Failed, spoilerpos = " + \
                        str(spoilerpos)

    helper.BAP_TIPP(app)

    BAP_LED = app.GetEnvvarValue("P_ASG_64_1_0_18_1")
    assert BAP_LED == 0, "2Check BAP LED"

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
           P.Tolerance, "2Zero position Failed, spoilerpos = " + \
                        str(spoilerpos)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 0, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 0, " 1AERO SETUP Failed, AERO SETUP Value = " + \
                                  str(AERO_SETUP_Value)


def test_704_NoUser():
    helper.STD_PRECONDITION(app, r)

    helper.BAP_START_SPOILER(app)

    time.sleep(1)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vMaxManMod / 3.6)

    time.sleep(1)

    BAP_MOD_REASON = app.GetEnvvarValue("P_ASG_64_1_0_19_2")
    assert BAP_MOD_REASON == 1, "1Check BAP_MOD_REASON"

    BAP_MOD_STATE = app.GetEnvvarValue("P_ASG_64_1_0_19_3_0")
    assert BAP_MOD_STATE == 0, "1Check BAP_MOD_STATE"

    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.vFzgManModSperrungInaktiv / 3.6, accel=5, update_rate=10)
    time.sleep(1)

    BAP_MOD_REASON = app.GetEnvvarValue("P_ASG_64_1_0_19_2")
    assert BAP_MOD_REASON == 0, "2Check BAP_MOD_REASON"

    BAP_MOD_STATE = app.GetEnvvarValue("P_ASG_64_1_0_19_3_0")
    assert BAP_MOD_STATE == 1, "2Check BAP_MOD_STATE"


def test_705_NoUser():
    helper.STD_PRECONDITION(app, r)

    helper.BAP_START_SPOILER(app)

    helper.SAD_OPEN(app)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.vthresh_sad_perfotox / 3.6, accel=5, update_rate=10)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 39, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 39, "1AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
           P.Tolerance, "1Zero position Failed, spoilerpos = " + \
                        str(spoilerpos)

    helper.BAP_TIPP(app)

    time.sleep(2)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 38, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 38, "2AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
           P.Tolerance, "2Zero position Failed, spoilerpos = " + \
                        str(spoilerpos)

    BAP_LED = app.GetEnvvarValue("P_ASG_64_1_0_18_1")
    assert BAP_LED == 1, "1Check BAP LED"

    helper.BAP_TIPP(app)

    time.sleep(2)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
           P.Tolerance, "3Zero position Failed, spoilerpos = " + \
                        str(spoilerpos)

    BAP_LED = app.GetEnvvarValue("P_ASG_64_1_0_18_1")
    assert BAP_LED == 0, "2Check BAP LED"


def test_706_NoUser():
    helper.STD_PRECONDITION(app, r)

    helper.BAP_START_SPOILER(app)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.vthresh_normal_min_move / 3.6, accel=5, update_rate=10)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 0, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 0, "1AERO SETUP Failed, AERO SETUP Value = " + \
                                  str(AERO_SETUP_Value)

    helper.BAP_TIPP(app)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 35, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 35, "2AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    helper.BAP_TIPP(app)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 0, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 0, "3AERO SETUP Failed, AERO SETUP Value = " + \
                                  str(AERO_SETUP_Value)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sport)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 5, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 5, "4AERO SETUP Failed, AERO SETUP Value = " + \
                                  str(AERO_SETUP_Value)

    helper.BAP_TIPP(app)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 35, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 35, "5AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    helper.BAP_TIPP(app)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 5, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 5, "6AERO SETUP Failed, AERO SETUP Value = " + \
                                  str(AERO_SETUP_Value)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sportplus)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 10, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 10, "7AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    helper.BAP_TIPP(app)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 35, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 35, "8AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    helper.BAP_TIPP(app)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 10, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 10, "9AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_offroad)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 15, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 15, "10AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    helper.BAP_TIPP(app)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 35, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 35, "11AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    helper.BAP_TIPP(app)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 15, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 15, "12AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)


def test_707_NoUser():
    helper.STD_PRECONDITION(app, r)

    helper.BAP_START_SPOILER(app)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.vthresh_normal_min_move / 3.6, accel=5, update_rate=10)

    helper.BAP_TIPP(app)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 35, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 35, "1AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sport)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 5, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 5, "2AERO SETUP Failed, AERO SETUP Value = " + \
                                  str(AERO_SETUP_Value)

    helper.BAP_TIPP(app)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 35, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 5, "3AERO SETUP Failed, AERO SETUP Value = " + \
                                  str(AERO_SETUP_Value)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sportplus)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 10, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 10, "4AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    helper.BAP_TIPP(app)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 35, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 35, "5AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_offroad)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 15, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 15, "6AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    helper.BAP_TIPP(app)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 35, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 35, "7AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_normal)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 0, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 0, "8AERO SETUP Failed, AERO SETUP Value = " + \
                                  str(AERO_SETUP_Value)


def test_708_NoUser():
    helper.STD_PRECONDITION(app, r)

    helper.BAP_START_SPOILER(app)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.vthresh_normal_min_move / 3.6, accel=5, update_rate=10)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 0, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 0, "1AERO SETUP Failed, AERO SETUP Value = " + \
                                  str(AERO_SETUP_Value)

    helper.BAP_TIPP(app)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 35, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 35, "2AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    helper.CHA_PROF_CHANGED(app)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 0, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 0, "3AERO SETUP Failed, AERO SETUP Value = " + \
                                  str(AERO_SETUP_Value)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sport)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 5, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 5, "4AERO SETUP Failed, AERO SETUP Value = " + \
                                  str(AERO_SETUP_Value)

    helper.BAP_TIPP(app)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 35, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 35, "5AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    helper.CHA_PROF_CHANGED(app)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 5, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 5, "6AERO SETUP Failed, AERO SETUP Value = " + \
                                  str(AERO_SETUP_Value)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sportplus)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 10, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 10, "7AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    helper.BAP_TIPP(app)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 35, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 35, "8AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    helper.CHA_PROF_CHANGED(app)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 10, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 10, "9AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_offroad)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 15, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 15, "10AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    helper.BAP_TIPP(app)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 35, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 35, "11AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    helper.CHA_PROF_CHANGED(app)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 15, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 15, "12AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)


def test_709_NoUser():
    helper.STD_PRECONDITION(app, r)

    helper.SAD_OPEN(app)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.vthresh_normal_min_move / 3.6, accel=5, update_rate=10)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 0, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 0, "1AERO SETUP Failed, AERO SETUP Value = " + \
                                  str(AERO_SETUP_Value)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
           P.Tolerance, "1Zero position Failed, spoilerpos = " + \
                        str(spoilerpos)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.Vthresh_SAD_Setup0to1 / 3.6, accel=5, update_rate=10)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 40, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 40, "2AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
           P.Tolerance, "2Perfo position Failed, spoilerpos = " + \
                        str(spoilerpos)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.Vthresh_SAD_Setup1to2 / 3.6, accel=5, update_rate=10)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 41, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 41, "3AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
           P.Tolerance, "3Perfo position Failed, spoilerpos = " + \
                        str(spoilerpos)

    AERO_REQ_SKE_Value = app.GetSignalValue(P.AERO_REQ_SKE['bus_type'], int(P.AERO_REQ_SKE['channel_num']),
                                            P.AERO_REQ_SKE['msg_name'],
                                            P.AERO_REQ_SKE['sig_name'])

    assert AERO_REQ_SKE_Value == 100, "1AERO_REQ_SKE Failed, AERO_REQ_SKE Value = " + \
                                      str(AERO_REQ_SKE_Value)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.Vthresh_SAD_Setup2to1 / 3.6, accel=5, update_rate=10)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 40, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 40, "4AERO SETUP Failed, AERO SETUP Value = " + \
                                   str(AERO_SETUP_Value)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
           P.Tolerance, "4Perfo position Failed, spoilerpos = " + \
                        str(spoilerpos)

    AERO_REQ_SKE_Value = app.GetSignalValue(P.AERO_REQ_SKE['bus_type'], int(P.AERO_REQ_SKE['channel_num']),
                                            P.AERO_REQ_SKE['msg_name'],
                                            P.AERO_REQ_SKE['sig_name'])

    assert AERO_REQ_SKE_Value == 126, "2AERO_REQ_SKE Failed, AERO_REQ_SKE Value = " + \
                                      str(AERO_REQ_SKE_Value)

    helper.speedramp(app, P.ACTUAL_SPEED,
                     P.Vthresh_SAD_Setup1to0 / 3.6, accel=5, update_rate=10)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 1, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 1, "5AERO SETUP Failed, AERO SETUP Value = " + \
                                  str(AERO_SETUP_Value)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
           P.Tolerance, "5Eco position Failed, spoilerpos = " + \
                        str(spoilerpos)

    AERO_REQ_SKE_Value = app.GetSignalValue(P.AERO_REQ_SKE['bus_type'], int(P.AERO_REQ_SKE['channel_num']),
                                            P.AERO_REQ_SKE['msg_name'],
                                            P.AERO_REQ_SKE['sig_name'])

    assert AERO_REQ_SKE_Value == 126, "3AERO_REQ_SKE Failed, AERO_REQ_SKE Value = " + \
                                      str(AERO_REQ_SKE_Value)
