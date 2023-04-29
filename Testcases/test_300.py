# import win32com.client
# import win32com.client.connect
from math import ceil
import time
import ast
import CANoe
import helper
import parameters as P
from riden import Riden
app = CANoe.CanoeSync()
r = helper.Riden_Connect()
if app == None:
    app.Load(
        r"\Projects\Spoiler\CANoe_Simulation_SX_400_v6.3\01_Configuration\HCP4_v13_Testing.cfg")
'''else:
    app.Stop()
    app.Load(
        r"\Projects\Spoiler\CANoe_Simulation_SX_400_v6.3\01_Configuration\HCP4_v13_Testing.cfg")'''

while(app == None):
    pass  # Do nothing in particular while app is loading

app.Start()

time.sleep(5)


def test_301_NoUser():
    # Drive Mode DM_normal

    helper.STD_PRECONDITION(app, r)
    time.sleep(1)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'],  127.7991)

    time.sleep(5)

    #spoilerpos = app.GetSignalValue("LIN", 7, "SP_01s_01", "SA1_Ist_Pos")

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.PERFO_POS, deviation=10, timeout=10)

    assert P.PERFO_POS - P.Tolerance < spoilerpos < P.PERFO_POS + \
        P.Tolerance, "1Zero to Perfo position Failed, spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], 8)

    time.sleep(5)

    #spoilerpos = app.GetSignalValue("LIN", 7, "SP_01s_01", "SA1_Ist_Pos")

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
        P.Tolerance, "2Perfo to Zero position Failed, spoilerpos = " + \
        str(spoilerpos)

    time.sleep(5)

    app.Stop()
