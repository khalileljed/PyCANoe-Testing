# import win32com.client
# import win32com.client.connect

import time

import parameters as P
import CANoe
import helper
from riden import Riden
# These are the default values for port, baudrate, and address
r = helper.Riden_Connect()
app = CANoe.CanoeSync()

if app == None:
    app.Load(
        r"\Projects\Spoiler\CANoe_Simulation_SX_420\01_Configuration\HCP4_v13_DynTrace_PrivateCAN_BAP_GR.cfg")
'''else:
    app.Stop()
    app.Load(
       r"\Projects\Spoiler\CANoe_Simulation_SX_420\01_Configuration\HCP4_v13_DynTrace_PrivateCAN_BAP_GR.cfg")'''

while(app == None):
    pass  # Do nothing in particular while app is loading

app.Start()

time.sleep(5)


def test_101_NoUser():
    # Drive Mode P.DM_normal

    helper.STD_PRECONDITION(app, r)

    time.sleep(1)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_normal_0toeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
        P.Tolerance, "1Zero to Eco position Failed, spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_normal_ecotoperfo / 3.6)

    time.sleep(5)

    #spoilerpos = app.GetSignalValue("LIN", 7, "SP_01s_01", "SA1_Ist_Pos")

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
        P.Tolerance, "2Eco to Perfo position Failed, spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_normal_perfotoeco / 3.6)

    time.sleep(5)

    #spoilerpos = app.GetSignalValue("LIN", 7, "SP_01s_01", "SA1_Ist_Pos")

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
        P.Tolerance, "3Perfo to Eco position Failed, spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_normal_ecoto0 / 3.6)

    time.sleep(5)

    #spoilerpos = app.GetSignalValue("LIN", 7, "SP_01s_01", "SA1_Ist_Pos")

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
        P.Tolerance, "4Eco to Zero position Failed, spoilerpos = " + \
        str(spoilerpos)


def test_102_NoUser():
    # Drive Mode P.DM_sport

    helper.STD_PRECONDITION(app, r)
    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sport)

    time.sleep(1)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_sport_0toeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
        P.Tolerance, "Zero to Eco position Failed"

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_sport_ecotoperfo / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
        P.Tolerance, "Eco to Perfo position Failed"

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_sport_perfotoeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
        P.Tolerance, "Perfo to Eco position Failed"

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_sport_ecoto0 / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
        P.Tolerance, "Eco to Zero position Failed"


def test_103_NoUser():
    # Drive Mode P.DM_sportplus
    helper.STD_PRECONDITION(app, r)
    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sportplus)

    time.sleep(1)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_splus_0toeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
        P.Tolerance, "Zero to Eco position Failed"

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_splus_ecotoperfo / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
        P.Tolerance, "Eco to Perfo position Failed"

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_splus_perfotoeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
        P.Tolerance, "Perfo to Eco position Failed"

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_splus_ecoto0 / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
        P.Tolerance, "Eco to Zero position Failed"


def test_104_NoUser():
    # Switch Drive Mode from P.DM_normal to P.DM_sportplus
    helper.STD_PRECONDITION(app, r)

    time.sleep(1)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_normal_0toeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
        P.Tolerance, "Zero to Eco position Failed, P.DM_normal , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_splus_ecotoperfo / 3.6)

    time.sleep(5)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sportplus)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
        P.Tolerance, "Eco to Perfo position Failed, P.DM_sportplus , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_splus_perfotoeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
        P.Tolerance, "Perfo to Eco position Failed, P.DM_sportplus , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_splus_ecoto0 / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
        P.Tolerance, "Eco to Zero position Failed, P.DM_sportplus , spoilerpos = " + \
        str(spoilerpos)


def test_105_NoUser():
    # Switch Drive Mode from P.DM_sportplus to P.DM_normal
    helper.STD_PRECONDITION(app, r)
    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sportplus)

    time.sleep(1)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_splus_0toeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
        P.Tolerance, "Zero to Eco position Failed, P.DM_sportplus , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_splus_ecotoperfo / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
        P.Tolerance, "Eco to Perfo Failed, P.DM_sportplus , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_normal)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
        P.Tolerance, "Perfo to Eco Failed, P.DM_normal , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_normal_ecotoperfo / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
        P.Tolerance, "Eco to Perfo Failed, P.DM_normal , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_normal_perfotoeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
        P.Tolerance, "Perfo to Eco position Failed, P.DM_normal , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_normal_ecoto0 / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
        P.Tolerance, "Eco to Zero position Failed, P.DM_normal , spoilerpos = " + \
        str(spoilerpos)


def test_106_NoUser():
    # Switch Drive Mode from P.DM_sport to P.DM_sportplus
    helper.STD_PRECONDITION(app, r)

    time.sleep(1)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sport)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_sport_0toeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
        P.Tolerance, "Zero to Eco position Failed, P.DM_normal , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_splus_ecotoperfo / 3.6)

    time.sleep(5)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sportplus)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
        P.Tolerance, "Eco to Perfo position Failed, P.DM_sportplus , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_splus_perfotoeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
        P.Tolerance, "Perfo to Eco position Failed, P.DM_sportplus , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_splus_ecoto0 / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
        P.Tolerance, "Eco to Zero position Failed, P.DM_sportplus , spoilerpos = " + \
        str(spoilerpos)


def test_107_NoUser():
    # Switch Drive Mode from P.DM_sportplus to P.DM_sport
    helper.STD_PRECONDITION(app, r)
    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sportplus)

    time.sleep(1)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_splus_0toeco / 3.6)

    time.sleep(5)

    #spoilerpos = app.GetSignalValue("LIN", 7, "SP_01s_01", "SA1_Ist_Pos")

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
        P.Tolerance, "Zero to Eco position Failed, P.DM_sportplus , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_splus_ecotoperfo / 3.6)

    time.sleep(5)

    #spoilerpos = app.GetSignalValue("LIN", 7, "SP_01s_01", "SA1_Ist_Pos")

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
        P.Tolerance, "Eco to Perfo Failed, P.DM_sportplus , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sport)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
        P.Tolerance, "Perfo to Eco Failed, P.DM_normal , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_sport_ecotoperfo / 3.6)

    time.sleep(5)

    #spoilerpos = app.GetSignalValue("LIN", 7, "SP_01s_01", "SA1_Ist_Pos")

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
        P.Tolerance, "Eco to Perfo Failed, P.DM_normal , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_sport_perfotoeco / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
        P.Tolerance, "Perfo to Eco position Failed, P.DM_normal , spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], P.vthresh_sport_ecoto0 / 3.6)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
        P.Tolerance, "Eco to Zero position Failed, P.DM_normal , spoilerpos = " + \
        str(spoilerpos)


def test_108_NoUser():
    # "Change driving mode with speed > vMaxFahrProg

    helper.STD_PRECONDITION(app, r)

    time.sleep(1)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], (P.vMaxFahrProg -1) / 3.6)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
        P.Tolerance, "1Zero to Perfo position Failed, spoilerpos = " + \
        str(spoilerpos)

    time.sleep(1)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 3, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 3, " 1AERO_SETUP position Failed, AERO SETUP Value = " + \
        str(AERO_SETUP_Value)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sportplus)

    time.sleep(1)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 13, deviation=10, timeout=10)

    assert AERO_SETUP_Value == 13, " 2AERO_SETUP position Failed, AERO SETUP Value = " + \
        str(AERO_SETUP_Value)


def test_109_NoUser():
    # Fast braking

    helper.STD_PRECONDITION(app, r)

    time.sleep(1)

    #app.SetSignalValue("Ethernet", 1, "VDSO_01_XIX_VLAN_Komfort","VDSO_Vx6d_XIX_VDSO_01_XIX_VLAN_Komfort", 250/3.6)

    helper.speedramp(app, P.ACTUAL_SPEED, P.vmax/3.6, accel=5,update_rate=10)
    time.sleep(1)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
        P.Tolerance, "1Zero to Perfo position Failed, spoilerpos = " + \
        str(spoilerpos)

    helper.speedramp(app, P.ACTUAL_SPEED, 0, 10,update_rate=10)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
        P.Tolerance, "2Perfo to Zero position Failed, spoilerpos = " + \
        str(spoilerpos)


def test_110_NoUser():
    # Quick cycle of driving modes, end in same mode

    helper.STD_PRECONDITION(app, r)

    time.sleep(1)

    helper.speedramp(app, P.ACTUAL_SPEED, 100/3.6, accel=5,update_rate=10)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
        P.Tolerance, "1Zero to Eco position Failed, spoilerpos = " + \
        str(spoilerpos)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sport)

    time.sleep(0.1)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sportplus)

    time.sleep(0.1)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_offroad)

    time.sleep(0.1)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_normal)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
        P.Tolerance, "2Eco position Failed, spoilerpos = " + \
        str(spoilerpos)


def test_111_NoUser():
    # Quick cycle of driving modes, end in different mode

    helper.STD_PRECONDITION(app, r)

    time.sleep(1)

    helper.speedramp(app, P.ACTUAL_SPEED, 100/3.6, accel=5,update_rate=10)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
        P.Tolerance, "1Zero to Eco position Failed, spoilerpos = " + \
        str(spoilerpos)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sport)

    time.sleep(0.1)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sportplus)

    time.sleep(0.1)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_offroad)

    time.sleep(0.1)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_normal)

    time.sleep(0.1)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sportplus)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
        P.Tolerance, "2Eco to Perfo position Failed, spoilerpos = " + \
        str(spoilerpos)


def test_112_User():
    # Quick cycle of driving modes, end in same mode - standing still

    helper.STD_PRECONDITION(app, r)

    time.sleep(1)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sport)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
        P.Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    time.sleep(0.1)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sport)

    time.sleep(0.1)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sportplus)

    time.sleep(0.1)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_offroad)

    time.sleep(0.1)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_normal)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
        P.Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    AERO_1_ERROR_VALUE = helper.waitforsignal(
        app, P.AERO_1_ERROR, 0, deviation=10, timeout=10)

    assert AERO_1_ERROR_VALUE == 0


def test_113_User():
    # Quick cycle of driving modes, end in different mode - standing still

    helper.STD_PRECONDITION(app, r)

    time.sleep(1)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sport)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
        P.Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    time.sleep(0.1)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sport)

    time.sleep(0.1)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sportplus)

    time.sleep(0.1)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_offroad)

    time.sleep(0.1)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_normal)

    time.sleep(0.1)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sportplus)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
        P.Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    AERO_1_ERROR_VALUE = helper.waitforsignal(
        app, P.AERO_1_ERROR, 0, deviation=10, timeout=10)

    assert AERO_1_ERROR_VALUE == 0


def test_114_User():
    # Slow cycle of driving modes, standing

    helper.STD_PRECONDITION(app, r)

    time.sleep(1)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sport)

    time.sleep(2)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
        P.Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sport)

    time.sleep(2)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
        P.Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sportplus)

    time.sleep(2)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
        P.Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_offroad)

    time.sleep(2)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
        P.Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_normal)

    time.sleep(2)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
        P.Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sport)

    time.sleep(2)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
        P.Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sportplus)

    time.sleep(2)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
        P.Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_offroad)

    time.sleep(5)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
        P.Tolerance, "1Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    AERO_1_ERROR_VALUE = helper.waitforsignal(
        app, P.AERO_1_ERROR, 0, deviation=10, timeout=10)

    assert AERO_1_ERROR_VALUE == 0


def test_116_NoUser():

    helper.STD_PRECONDITION(app, r)
    
    helper.BAP_START_SPOILER(app)
    
    helper.speedramp(app, P.ACTUAL_SPEED, P.vthresh_normal_min_move/3.6, accel=5,update_rate=10)
    
    time.sleep(1)
    
    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, 0, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 0, " 1AERO_SETUP Failed, AERO SETUP Value = " + \
        str(AERO_SETUP_Value)
        
    BAP_LED = app.GetEnvvarValue("P_ASG_64_1_0_18_1")
    assert BAP_LED == 0, "Check BAP LED"
    
    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sport_ind)
    
    time.sleep(1)
    
    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, 31, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 31, " 2AERO_SETUP Failed, AERO SETUP Value = " + \
        str(AERO_SETUP_Value)
        
    BAP_LED = app.GetEnvvarValue("P_ASG_64_1_0_18_1")
    assert BAP_LED == 1, "Check BAP LED"
    
    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_offroad_ind)
    
    time.sleep(1)
    
    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, 31, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 31, " 3AERO_SETUP Failed, AERO SETUP Value = " + \
        str(AERO_SETUP_Value)
        
    BAP_LED = app.GetEnvvarValue("P_ASG_64_1_0_18_1")
    assert BAP_LED == 1, "Check BAP LED"
    
    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_sportplus_ind)
    
    time.sleep(1)
    
    AERO_SETUP_Value = helper.waitforsignal(app, P.AERO_SETUP, 31, deviation=0, timeout=10)

    assert AERO_SETUP_Value == 31, " 4AERO_SETUP Failed, AERO SETUP Value = " + \
        str(AERO_SETUP_Value)
        
    BAP_LED = app.GetEnvvarValue("P_ASG_64_1_0_18_1")
    assert BAP_LED == 1, "Check BAP LED"

    
# app.Stop()
