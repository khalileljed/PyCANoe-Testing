import configparser
import time
from math import ceil


def read_config():
    # Method to read config file settings

    config = configparser.ConfigParser()
    # full path here
    # config.read('C:/Users/ilyes/Desktop/AOLOA-Projects/PyCANoe-Testing/Examples/pytest/configurations.ini')
    config.read(
        'C:/Projects/PyCANoe-Testing/Examples/pytest/configurations.ini')
    return config


def waitforsignal(app, signal, value, deviation=0, timeout=10):
    # Waits for a signal to reach value. accepted deviation from value in percent.
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


def speedramp(app, signal, target_speed, accel=5):
    # Gets current speed value and ramps it up/down with accel m/s² . Default accel is 5 m/s².

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
                time.sleep(1)

            curr_speed -= (abs(target_speed-curr_speed) % accel)

            app.SetSignalValue(bus_type, channel_num,
                               msg_name, sig_name, curr_speed)
        else:
            for i in range(moves):
                curr_speed -= accel*1
                app.SetSignalValue(bus_type, channel_num,
                                   msg_name, sig_name, curr_speed)
                time.sleep(1)
    else:
        if abs(target_speed-curr_speed) % accel != 0:
            for i in range(moves-1):
                curr_speed += accel*1
                app.SetSignalValue(bus_type, channel_num,
                                   msg_name, sig_name, curr_speed)
                time.sleep(1)

            curr_speed += ((target_speed-curr_speed) % accel)

            app.SetSignalValue(bus_type, channel_num,
                               msg_name, sig_name, curr_speed)
        else:
            for i in range(moves):
                curr_speed += accel*1
                app.SetSignalValue(bus_type, channel_num,
                                   msg_name, sig_name, curr_speed)
                time.sleep(1)

def BAP_START_SPOILER(app):
    # Start and initialize Spoiler ASG
    app.SetEnvvarValue("ON_OFF_ASG64_1",1)
    app.SetEnvvarValue("C_ASG_64_1_0_1GetAll_BTN",1)
    app.SetEnvvarValue("C_ASG_64_1_0_1GetAll_BTN",0)
