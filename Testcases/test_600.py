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

while(app == None):
    pass  # Do nothing in particular while app is loading

app.Start()

time.sleep(5)

def test_601_User():
    # Clamp 15 is turned off and on again.

    helper.STD_PRECONDITION(app,r)

    time.sleep(1)

    x = helper.Mbox('PSF Tester', 'Press OK if CLAMP15 is OFF: ', 1)
    assert x == 1, "Test Failed check CLAMP15"
    time.sleep(5)
    y = helper.Mbox('PSF Tester', 'Press OK if CLAMP15 is ON: ', 1)
    assert y == 1, "Test Failed check CLAMP15"
    time.sleep(5)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 17, deviation=100, timeout=10)

    assert 0 <= AERO_SETUP_Value <= 34, " AERO SETUP Failed, AERO SETUP Value = " + \
        str(AERO_SETUP_Value)


def test_602_NoUser():
    # Clamp 30 is turned off and on again.

    helper.STD_PRECONDITION(app,r)

    time.sleep(1)

    r.set_output(False)
    time.sleep(5)
    r.set_output(True)
    time.sleep(10)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 17, deviation=100, timeout=10)

    assert 0 <= AERO_SETUP_Value <= 34, " AERO SETUP Failed, AERO SETUP Value = " + \
        str(AERO_SETUP_Value)


def test_603_User():
    # Startup clamp 15 on, from manual mode

    helper.STD_PRECONDITION(app,r)
    
    helper.BAP_START_SPOILER(app)
    time.sleep(1)
    
    app.SetSysvarValue("AeroFkt::HMI", "SpoilerActuation_Actuation", 1)
    time.sleep(0.3)
    app.SetSysvarValue("AeroFkt::HMI", "SpoilerActuation_Actuation", 0)

    time.sleep(1)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 35, deviation=0, timeout=10)

    assert 35 <= AERO_SETUP_Value <= 38, " 1AERO SETUP Failed, AERO SETUP Value = " + \
        str(AERO_SETUP_Value)
        
    BAP_LED = app.GetEnvvarValue("P_ASG_64_1_0_18_1")
    assert BAP_LED == 1, "1Check BAP LED"

    x = helper.Mbox('PSF Tester', 'Press OK if CLAMP15 is OFF: ', 1)
    assert x == 1, "1Test Failed check CLAMP15"
    
    time.sleep(5)
    
    y = helper.Mbox('PSF Tester', 'Press OK if CLAMP15 is ON: ', 1)
    assert y == 1, "2Test Failed check CLAMP15"
    
    time.sleep(5)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 17, deviation=100, timeout=10)

    assert 0 <= AERO_SETUP_Value <= 34, " 2AERO SETUP Failed, AERO SETUP Value = " + \
        str(AERO_SETUP_Value)
        
    BAP_LED = app.GetEnvvarValue("P_ASG_64_1_0_18_1")
    assert BAP_LED == 1, "2Check BAP LED"
    
    helper.speedramp(app, P.ACTUAL_SPEED, (P.vTippTast+1)/3.6, accel=5,update_rate=10)
    
    BAP_LED = app.GetEnvvarValue("P_ASG_64_1_0_18_1")
    assert BAP_LED == 0, "3Check BAP LED"
    

def test_604_NoUser():
    # Startup clamp 30 on, from manual mode

    helper.STD_PRECONDITION(app,r)
    
    helper.BAP_START_SPOILER(app)
    time.sleep(1)
    
    app.SetSysvarValue("AeroFkt::HMI", "SpoilerActuation_Actuation", 1)
    time.sleep(0.3)
    app.SetSysvarValue("AeroFkt::HMI", "SpoilerActuation_Actuation", 0)

    time.sleep(1)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 36.5, deviation=4.3, timeout=10)

    assert 35 <= AERO_SETUP_Value <= 38, " AERO SETUP Failed, AERO SETUP Value = " + \
        str(AERO_SETUP_Value)

    r.set_output(False)
    time.sleep(5)
    r.set_output(True)
    time.sleep(10)

    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 17, deviation=100, timeout=10)

    assert 0 <= AERO_SETUP_Value <= 34, " AERO SETUP Failed, AERO SETUP Value = " + \
        str(AERO_SETUP_Value)


def test_605_NoUser():
    # Finish movement with speed < v_TippTast
    pytest.skip('Test can not be executet because of Dataset-Values.') # Test can not be executet because of Dataset-Values.
    
    helper.STD_PRECONDITION(app,r)
    helper.BAP_START_SPOILER(app)
    time.sleep(1)
    
    helper.speedramp(app, P.ACTUAL_SPEED, (vTippTast+5)/3.6, accel=5,update_rate=10)
    
    time.sleep(1)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
        P.Tolerance, "1Zero to Eco position Failed, spoilerpos = " + \
        str(spoilerpos)
    
    time.sleep(2)
    
    app.SetSysvarValue("AeroFkt::HMI", "SpoilerActuation_Actuation", 1)
    time.sleep(0.2)
    app.SetSysvarValue("AeroFkt::HMI", "SpoilerActuation_Actuation", 0)
    time.sleep(0.2)
    
    helper.speedramp(app, P.ACTUAL_SPEED, (vTippTast-5)/3.6, accel=5,update_rate=10)
    
    time.sleep(1)
    
    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
        P.Tolerance, "2Eco to Perfo position Failed, spoilerpos = " + \
        str(spoilerpos)
        
    time.sleep(2)


def test_606_User():
    # Finish movement on clamp15 off

    helper.STD_PRECONDITION(app,r)    

    time.sleep(1)
    
    helper.speedramp(app, P.ACTUAL_SPEED, P.vthresh_normal_ecotoperfo/3.6, accel=5,update_rate=10)
    
    time.sleep(1)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
        P.Tolerance, "1Zero to Perfo position Failed, spoilerpos = " + \
        str(spoilerpos)
        
    helper.Mbox('PSF Tester', 'Press OK and immediatly after turn CLAMP15 OFF.', 1)
    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                    P.ACTUAL_SPEED['sig_name'], P.vthresh_normal_min_move/3.6)

    time.sleep(5)
    
    
    x = helper.Mbox('PSF Tester', 'Did the spoiler actuator finish its movement to ZERO_POS?', 4)

    assert x == 1, "Actuator did not finish movement."
    
    helper.CL15_POSTCONDITION()


def test_607_User():
    
    helper.STD_PRECONDITION(app,r)
    
    helper.BAP_START_SPOILER(app)
    time.sleep(1)
    
    app.SetSysvarValue("AeroFkt::HMI", "SpoilerActuation_Actuation", 1)
    time.sleep(0.3)
    app.SetSysvarValue("AeroFkt::HMI", "SpoilerActuation_Actuation", 0)

    time.sleep(1)
    
    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 35, deviation=0, timeout=5)

    assert  AERO_SETUP_Value == 35, " 1AERO SETUP Failed, AERO SETUP Value = " + \
        str(AERO_SETUP_Value)
        
    BAP_LED = app.GetEnvvarValue("P_ASG_64_1_0_18_1")
    assert BAP_LED == 1, "1Check BAP LED"
    
    helper.BAP_TAST(app,1)

    x = helper.Mbox('PSF Tester', 'Press OK if CLAMP15 is OFF: ', 1)
    assert x == 1, "1Test Failed check CLAMP15"
    
    time.sleep(5)
    
    y = helper.Mbox('PSF Tester', 'Press OK if CLAMP15 is ON: ', 1)
    assert y == 1, "2Test Failed check CLAMP15"
    
    time.sleep(1)
    
    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 0, deviation=0, timeout=10)

    assert  AERO_SETUP_Value == 0, " 2AERO SETUP Failed, AERO SETUP Value = " + \
        str(AERO_SETUP_Value)
        
    BAP_LED = app.GetEnvvarValue("P_ASG_64_1_0_18_1")
    assert BAP_LED == 3, "2Check BAP LED"
    
    helper.BAP_TIPP(app)
    
    AERO_SETUP_Value = helper.waitforsignal(
        app, P.AERO_SETUP, 35, deviation=0, timeout=5)

    assert  AERO_SETUP_Value == 35, " 3AERO SETUP Failed, AERO SETUP Value = " + \
        str(AERO_SETUP_Value)