import configparser
import time
from math import ceil
import ctypes  # An included library with Python install.
import parameters as P
from riden import Riden

""" 
    Helper functions
"""

def Riden_Connect():
    try:
        return Riden(port="COM9", baudrate=115200, address=1)
    except FileNotFoundError:
        x = Mbox('Error', 'File Not Found', 1)
        return x
    except PermissionError:
        x = Mbox('Error', 'Permission Denied', 1)
        return x
    except:
        x = Mbox('Error', 'Something else went wrong', 1)
        return x


def waitforsignal(app, signal, value, deviation=0, timeout=10):
    #Waits for a signal to reach value. accepted deviation from value in percent.
    # Fail after timeout. Standard values for deviation is 0 and for timeout is 10 seconds.

    bus_type = signal['bus_type']
    channel_num = int(signal['channel_num'])
    msg_name = signal['msg_name']
    sig_name = signal['sig_name']
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


def speedramp(app, signal, target_speed, accel=5, update_rate=10):
    # Gets current speed value and ramps it up/down with accel m/s² . Default accel is 5 m/s².

    accel = accel/update_rate

    bus_type = signal['bus_type']
    channel_num = int(signal['channel_num'])
    msg_name = signal['msg_name']
    sig_name = signal['sig_name']

    curr_speed = app.GetSignalValue(bus_type, channel_num, msg_name, sig_name)

    moves = ceil(abs(target_speed-curr_speed)/accel)

    if target_speed < curr_speed:
        if abs(target_speed-curr_speed) % accel != 0:
            for i in range(moves-1):
                curr_speed -= accel*1
                app.SetSignalValue(bus_type, channel_num,
                                   msg_name, sig_name, curr_speed)
                time.sleep(1/update_rate)

            curr_speed -= (abs(target_speed-curr_speed) % accel)

            app.SetSignalValue(bus_type, channel_num,
                               msg_name, sig_name, curr_speed)
        else:
            for i in range(moves):
                curr_speed -= accel*1
                app.SetSignalValue(bus_type, channel_num,
                                   msg_name, sig_name, curr_speed)
                time.sleep(1/update_rate)
    else:
        if abs(target_speed-curr_speed) % accel != 0:
            for i in range(moves-1):
                curr_speed += accel*1
                app.SetSignalValue(bus_type, channel_num,
                                   msg_name, sig_name, curr_speed)
                time.sleep(1/update_rate)

            curr_speed += ((target_speed-curr_speed) % accel)

            app.SetSignalValue(bus_type, channel_num,
                               msg_name, sig_name, curr_speed)
        else:
            for i in range(moves):
                curr_speed += accel*1
                app.SetSignalValue(bus_type, channel_num,
                                   msg_name, sig_name, curr_speed)
                time.sleep(1/update_rate)


def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def BAP_TAST(app, seconds):

    app.SetSysvarValue("AeroFkt::HMI", "SpoilerActuation_Actuation", 1)
    time.sleep(seconds)
    app.SetSysvarValue("AeroFkt::HMI", "SpoilerActuation_Actuation", 0)


def BAP_TIPP(app):

    app.SetSysvarValue("AeroFkt::HMI", "SpoilerActuation_Actuation", 1)
    time.sleep(0.3)
    app.SetSysvarValue("AeroFkt::HMI", "SpoilerActuation_Actuation", 0)


def SAD_OPEN(app):

    # P.SUNROOF_POS
    app.SetSignalValue(P.SUNROOF_POS['bus_type'], int(P.SUNROOF_POS['channel_num']), P.SUNROOF_POS['msg_name'],
                       P.SUNROOF_POS['sig_name'], 120)

    # P.SUNROOF_LAGE
    app.SetSignalValue(P.SUNROOF_LAGE['bus_type'], int(P.SUNROOF_LAGE['channel_num']), P.SUNROOF_LAGE['msg_name'],
                       P.SUNROOF_LAGE['sig_name'], 1)


def CHA_PROF_CHANGED(app):

    app.SetSignalValue(P.CHA_PROFCHNGD['bus_type'], int(P.CHA_PROFCHNGD['channel_num']), P.CHA_PROFCHNGD['msg_name'],
                       P.CHA_PROFCHNGD['sig_name'], 1)

    time.sleep(0.3)

    app.SetSignalValue(P.CHA_PROFCHNGD['bus_type'], int(P.CHA_PROFCHNGD['channel_num']), P.CHA_PROFCHNGD['msg_name'],
                       P.CHA_PROFCHNGD['sig_name'], 0)

""" 
    Precondition Blocks
"""


def BAP_START_SPOILER(app):
    # Start and initialize Spoiler ASG
    app.SetEnvvarValue("ON_OFF_ASG64_1", 1)
    time.sleep(1)
    app.SetEnvvarValue("C_ASG_64_1_0_1GetAll_BTN", 1)
    time.sleep(0.5)
    app.SetEnvvarValue("C_ASG_64_1_0_1GetAll_BTN", 0)


def STD_PRECONDITION(app, r):

    r.set_output(False)
    time.sleep(1)
    r.set_output(True)
    time.sleep(1)

    # Set SimulationControl to "send all messages" (Restbus Main Panel)
    app.SetSysvarValue("SimulationControl", "sv_SimulationControl", 1)

    # Precondition

    app.SetSignalValue(P.DriveMode['bus_type'], int(P.DriveMode['channel_num']), P.DriveMode['msg_name'],
                       P.DriveMode['sig_name'], P.DM_normal)

    app.SetSignalValue(P.LAUNCH['bus_type'], int(P.LAUNCH['channel_num']), P.LAUNCH['msg_name'],
                       P.LAUNCH['sig_name'], P.launch_init)

    # P.SUNROOF_POS
    app.SetSignalValue(P.SUNROOF_POS['bus_type'], int(P.SUNROOF_POS['channel_num']), P.SUNROOF_POS['msg_name'],
                       P.SUNROOF_POS['sig_name'], 0)

    # P.SUNROOF_LAGE
    app.SetSignalValue(P.SUNROOF_LAGE['bus_type'], int(P.SUNROOF_LAGE['channel_num']), P.SUNROOF_LAGE['msg_name'],
                       P.SUNROOF_LAGE['sig_name'], 0)

    # allow spoiler to move to zero_pos by setting speed = 9 ACTUAL_SPEED
    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], 9)

    spoilerpos = waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], 0)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
        P.Tolerance, "Precondition Failed, spoilerpos = " + str(spoilerpos)


def CL15_POSTCONDITION():
    x = Mbox('PSF Tester', 'Turn CLAMP15 ON.', 1)
    assert x == 1, "Test Failed check CLAMP15"
