import time

import parameters as P
import CANoe
import helper
from riden import Riden
# These are the default values for port, baudrate, and address
r = helper.Riden_Connect()
app = CANoe.CanoeSync()


def Precondition_Mustermappe(Drehrichtung, Initialisiert, Referenziert, SpoilerPos, Pos_erreicht):

    # allow spoiler to move to zero_pos by setting speed = 9 ACTUAL_SPEED
    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], 9)

    app.SetSignalValue(P.ACTUAL_SPEED['bus_type'], int(P.ACTUAL_SPEED['channel_num']), P.ACTUAL_SPEED['msg_name'],
                       P.ACTUAL_SPEED['sig_name'], 0)

    app.SetSignalValue(P.ACTUAL_Drehrichtung['bus_type'], int(P.ACTUAL_Drehrichtung['channel_num']), P.ACTUAL_Drehrichtung['msg_name'],
                       P.ACTUAL_Drehrichtung['sig_name'], Drehrichtung)

    app.SetSignalValue(P.Spoi_Initialisiert['bus_type'], int(P.Spoi_Initialisiert['channel_num']), P.Spoi_Initialisiert['msg_name'],
                       P.Spoi_Initialisiert['sig_name'], Initialisiert)

    app.SetSignalValue(P.Spoi_Referenziert['bus_type'], int(P.Spoi_Referenziert['channel_num']), P.Spoi_Referenziert['msg_name'],
                       P.Spoi_Referenziert['sig_name'], Referenziert)

    app.SetSignalValue(P.ACTUAL_POS['bus_type'], int(P.ACTUAL_POS['channel_num']), P.ACTUAL_POS['msg_name'],
                       P.ACTUAL_POS['sig_name'], SpoilerPos)

    app.SetSignalValue(P.Spoi_Pos_erreicht['bus_type'], int(P.Spoi_Pos_erreicht['channel_num']), P.Spoi_Pos_erreicht['msg_name'],
                       P.Spoi_Pos_erreicht['sig_name'], Pos_erreicht)


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


def test_PSF_IT_1_1():

    Precondition_Mustermappe(3, 1, 1, 160, 1)

    time.sleep(1)
    helper.speedramp(app, P.ACTUAL_SPEED, 15.5, accel=7.75, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
        P.Tolerance, "1Zero to Eco position Failed, spoilerpos = " + \
        str(spoilerpos)

    Freigabe_Verst = app.GetSignalValue(
        'LIN', 7, 'SP_01e_01', 'MA_SA1_Freigabe_Verst')

    assert Freigabe_Verst == 1, "1Freigabe Verst Failed, Freigabe Verst = " + \
        str(Freigabe_Verst)

    app.SetSignalValue('LIN', 7, 'SP_01s_01', 'SA1_Pos_erreicht', 0)

    app.SetSignalValue(P.ACTUAL_POS['bus_type'], int(
        P.ACTUAL_POS['channel_num']), P.ACTUAL_POS['msg_name'], P.ACTUAL_POS['sig_name'], 1360)
    time.sleep(2)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
        P.Tolerance, "2Eco position Failed, spoilerpos = " + \
        str(spoilerpos)

    app.SetSignalValue('LIN', 7, 'SP_01s_01', 'SA1_Pos_erreicht', 1)

    Freigabe_Verst = app.GetSignalValue(
        'LIN', 7, 'SP_01e_01', 'MA_SA1_Freigabe_Verst')

    assert Freigabe_Verst == 0, "2Freigabe Verst Failed, Freigabe Verst = " + \
        str(Freigabe_Verst)

    time.sleep(1)

    helper.speedramp(app, P.ACTUAL_SPEED, 9, accel=6.5, update_rate=10)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ZERO_POS, deviation=10, timeout=10)

    assert P.ZERO_POS - P.Tolerance < spoilerpos < P.ZERO_POS + \
        P.Tolerance, "1Zero to Eco position Failed, spoilerpos = " + \
        str(spoilerpos)

    Freigabe_Verst = app.GetSignalValue(
        'LIN', 7, 'SP_01e_01', 'MA_SA1_Freigabe_Verst')

    assert Freigabe_Verst == 1, "1Freigabe Verst Failed, Freigabe Verst = " + \
        str(Freigabe_Verst)

    app.SetSignalValue('LIN', 7, 'SP_01s_01', 'SA1_Pos_erreicht', 0)

    app.SetSignalValue(P.ACTUAL_POS['bus_type'], int(
        P.ACTUAL_POS['channel_num']), P.ACTUAL_POS['msg_name'], P.ACTUAL_POS['sig_name'], 160)
    time.sleep(2)

    spoilerpos = helper.waitforsignal(
        app, P.ACTUAL_POS, P.ECO_POS, deviation=10, timeout=10)

    assert P.ECO_POS - P.Tolerance < spoilerpos < P.ECO_POS + \
        P.Tolerance, "2Eco position Failed, spoilerpos = " + \
        str(spoilerpos)

    app.SetSignalValue('LIN', 7, 'SP_01s_01', 'SA1_Pos_erreicht', 1)

    Freigabe_Verst = app.GetSignalValue(
        'LIN', 7, 'SP_01e_01', 'MA_SA1_Freigabe_Verst')

    assert Freigabe_Verst == 0, "2Freigabe Verst Failed, Freigabe Verst = " + \
        str(Freigabe_Verst)


def test_PSF_IT_2_1():

    Precondition_Mustermappe(3, 0, 0, 4095, 1)

    time.sleep(1)

    app.SetSignalValue(P.Spoi_Pos_erreicht['bus_type'], int(
        P.Spoi_Pos_erreicht['channel_num']), P.Spoi_Pos_erreicht['msg_name'], P.Spoi_Pos_erreicht['sig_name'], 0)

    time.sleep(1)

    Soll_Pos_Val = app.GetSignalValue(P.Soll_Pos['bus_type'], int(
        P.Soll_Pos['channel_num']), P.Soll_Pos['msg_name'], P.Soll_Pos['sig_name'])

    assert Soll_Pos_Val == 0, "1Soll_Pos Verst Failed, Freigabe Verst = " + \
        str(Soll_Pos_Val)

    Freigabe_Verst_Val = app.GetSignalValue(P.Freigabe_Verst['bus_type'], int(
        P.Freigabe_Verst['channel_num']), P.Freigabe_Verst['msg_name'], P.Freigabe_Verst['sig_name'])

    assert Freigabe_Verst_Val == 1, "1Freigabe Failed, Freigabe Verst = " + \
        str(Freigabe_Verst_Val)

    Anf_Referenzierung_Val = app.GetSignalValue(P.Anf_Referenzierung['bus_type'], int(
        P.Anf_Referenzierung['channel_num']), P.Anf_Referenzierung['msg_name'], P.Anf_Referenzierung['sig_name'])

    assert Anf_Referenzierung_Val == 1, "1Anf_Referenzierung Failed, Freigabe Verst = " + \
        str(Anf_Referenzierung_Val)

    time.sleep(1)

    app.SetSignalValue(P.Spoi_Initialisiert['bus_type'], int(
        P.Spoi_Initialisiert['channel_num']), P.Spoi_Initialisiert['msg_name'], P.Spoi_Initialisiert['sig_name'], 1)

    app.SetSignalValue(P.Spoi_Referenziert['bus_type'], int(
        P.Spoi_Referenziert['channel_num']), P.Spoi_Referenziert['msg_name'], P.Spoi_Referenziert['sig_name'], 1)

    time.sleep(1)

    Soll_Pos_Val = app.GetSignalValue(P.Soll_Pos['bus_type'], int(
        P.Soll_Pos['channel_num']), P.Soll_Pos['msg_name'], P.Soll_Pos['sig_name'])

    assert Soll_Pos_Val == 160, "1Soll_Pos Verst Failed, Freigabe Verst = " + \
        str(Soll_Pos_Val)

    Freigabe_Verst_Val = app.GetSignalValue(P.Freigabe_Verst['bus_type'], int(
        P.Freigabe_Verst['channel_num']), P.Freigabe_Verst['msg_name'], P.Freigabe_Verst['sig_name'])

    assert Freigabe_Verst_Val == 1, "1Freigabe Failed, Freigabe Verst = " + \
        str(Freigabe_Verst_Val)

    Anf_Referenzierung_Val = app.GetSignalValue(P.Anf_Referenzierung['bus_type'], int(
        P.Anf_Referenzierung['channel_num']), P.Anf_Referenzierung['msg_name'], P.Anf_Referenzierung['sig_name'])

    assert Anf_Referenzierung_Val == 0, "1Anf_Referenzierung Failed, Freigabe Verst = " + \
        str(Anf_Referenzierung_Val)

    time.sleep(1)

    app.SetSignalValue(P.Spoi_Pos_erreicht['bus_type'], int(
        P.Spoi_Pos_erreicht['channel_num']), P.Spoi_Pos_erreicht['msg_name'], P.Spoi_Pos_erreicht['sig_name'], 1)

    app.SetSignalValue(P.ACTUAL_POS['bus_type'], int(
        P.ACTUAL_POS['channel_num']), P.ACTUAL_POS['msg_name'], P.ACTUAL_POS['sig_name'], 160)

    time.sleep(1)

    Soll_Pos_Val = app.GetSignalValue(P.Soll_Pos['bus_type'], int(
        P.Soll_Pos['channel_num']), P.Soll_Pos['msg_name'], P.Soll_Pos['sig_name'])

    assert Soll_Pos_Val == 160, "1Soll_Pos Verst Failed, Freigabe Verst = " + \
        str(Soll_Pos_Val)

    Freigabe_Verst_Val = app.GetSignalValue(P.Freigabe_Verst['bus_type'], int(
        P.Freigabe_Verst['channel_num']), P.Freigabe_Verst['msg_name'], P.Freigabe_Verst['sig_name'])

    assert Freigabe_Verst_Val == 0, "1Freigabe Failed, Freigabe Verst = " + \
        str(Freigabe_Verst_Val)

    Anf_Referenzierung_Val = app.GetSignalValue(P.Anf_Referenzierung['bus_type'], int(
        P.Anf_Referenzierung['channel_num']), P.Anf_Referenzierung['msg_name'], P.Anf_Referenzierung['sig_name'])

    assert Anf_Referenzierung_Val == 0, "1Anf_Referenzierung Failed, Freigabe Verst = " + \
        str(Anf_Referenzierung_Val)

def test_PSF_IT_3_1():
    
    Precondition_Mustermappe(3, 1, 1, 160, 1)

    time.sleep(1)
    
    
    #HCP4_VLAN_Komfort:SystemInfo_01:SI_P_Mode_gueltig = 0
    
    