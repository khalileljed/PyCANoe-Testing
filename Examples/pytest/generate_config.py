import configparser
# CREATE OBJECT
config_file = configparser.ConfigParser()

# ADD NEW SECTION AND SETTINGS
config_file["spoiler positions"] = {
    "ZERO_POS": 160,
    "ECO_POS": 1360,
    "PERFO_POS": 2120,
    "Tolerance": 50
}

config_file["Drivemodes"] = {
    "DM_normal": 2,
    "DM_sport": 3,
    "DM_sportplus": 6,
    "DM_offroad": 4
}

config_file["Launchcontrol values"] = {
    "launch_init": 0,
    "launch_prep": 1,
    "launch_active": 2,
    "Vthresh_launch_XtoECO":0,
    "Vthresh_launch_ECOtoPERFO":150
}

config_file["Speed thresholds normal"] = {
    "Vthresh_normal_min_move": 33,
    "Vthresh_normal_0toECO": 54,
    "Vthresh_normal_ECOto0": 34,
    "Vthresh_normal_ECOtoPERFO": 150,
    "Vthresh_normal_PERFOtoECO": 130
}

config_file["Speed thresholds sport"] = {
    "Vthresh_sport_min_move": 33,
    "Vthresh_sport_0toECO": 54,
    "Vthresh_sport_ECOto0": 34,
    "Vthresh_sport_ECOtoPERFO": 150,
    "Vthresh_sport_PERFOtoECO": 130
}

config_file["Speed thresholds offroad"] = {
    "Vthresh_offroad_min_move": 33,
    "Vthresh_offroad_0toECO": 54,
    "Vthresh_offroad_ECOto0": 34,
    "Vthresh_offroad_ECOtoPERFO": 150,
    "Vthresh_offroad_PERFOtoECO": 130
}

config_file["Speed thresholds sportplus"] = {
    "Vthresh_sPlus_min_move": 33,
    "Vthresh_sPlus_0toECO": 54,
    "Vthresh_sPlus_ECOto0": 34,
    "Vthresh_sPlus_ECOtoPERFO": 90,
    "Vthresh_sPlus_PERFOtoECO": 70
}

config_file["Speed thresholds individual"] = {
    "Vthresh_ind_min_move": 33,
    "Vthresh_ind_0toECO": 0,
    "Vthresh_ind_ECOto0": 0,
    "Vthresh_ind_ECOtoPERFO": 90,
    "Vthresh_ind_PERFOtoECO": 70
}

config_file["Speed thresholds manual"] = {
    "Vthresh_manual_min_move": 33,
    "Vthresh_manual_0toECO": 0,
    "Vthresh_manual_ECOto0": 0,
    "Vthresh_manual_ECOtoPERFO": 90,
    "Vthresh_manual_PERFOtoECO": 70
}



config_file["Signals"] = {
    "AERO_SETUP": {
        "bus_type": "Ethernet",
        "channel_num": 1,
        "msg_name": "Aero_04_XIX_VLAN_Komfort",
        "sig_name": "Aero_AktivesSetup_XIX_Aero_04_XIX_VLAN_Komfort"
    },
    "ACTUAL_POS": {
        "bus_type": "LIN",
        "channel_num": 7,
        "msg_name": "SP_01s_01",
        "sig_name": "SA1_Ist_Pos"
    },
    "ACTUAL_SPEED": {
        "bus_type": "Ethernet",
        "channel_num": 1,
        "msg_name": "VDSO_01_XIX_VLAN_Komfort",
        "sig_name": "VDSO_Vx6d_XIX_VDSO_01_XIX_VLAN_Komfort"
    },
    "LAUNCH": {
        "bus_type": "Ethernet",
        "channel_num": 1,
        "msg_name": "HCP1_09_XIX_VLAN_Komfort",
        "sig_name": "LnchCtl_StReq_XIX_HCP1_09_XIX_VLAN_Komfort"
    },
    "DriveMode": {
        "bus_type": "Ethernet",
        "channel_num": 1,
        "msg_name": "Charisma_20_XIX_VLAN_Komfort",
        "sig_name": "CHA_ReqPrgHsp_XIX_Charisma_20_XIX_VLAN_Komfort"

    },
    "AERO_1_ERROR": {
        "bus_type": "Ethernet",
        "channel_num": 1,
        "msg_name": "Aero_04_XIX_VLAN_Komfort",
        "sig_name": "Aero_System_1_Fehler_XIX_Aero_04_XIX_VLAN_Komfort"

    },
    "SUNROOF_POS": {
        "bus_type": "CAN",
        "channel_num": 2,
        "msg_name": "SAD_02_XIX_HCP4_CANFD02",
        "sig_name": "MD1_Position_XIX_SAD_02_XIX_HCP4_CANFD02"

    },
    "SUNROOF_LAGE": {
        "bus_type": "CAN",
        "channel_num": 2,
        "msg_name": "SAD_02_XIX_HCP4_CANFD02",
        "sig_name": "MD3_Lage_XIX_SAD_02_XIX_HCP4_CANFD02"

    }
}

config_file["SAD"] = {
    "Vthresh_SAD_XtoPERFO": 90,
    "Vthresh_SAD_PERFOtoX": 70,
    "Vmax": 250}



# SAVE CONFIG FILE
with open(r"C:/Users/ilyes/Desktop/AOLOA-Projects/PyCANoe-Testing/Examples/pytest/configurations.ini", 'w') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()

print("Config file 'configurations.ini' created")


"""
Adding/Updating settings in the config file    
    
import configparser

# CREATE OBJECT
config_file = configparser.ConfigParser()

# READ CONFIG FILE
config_file.read("configurations.ini")

# UPDATE A FIELD VALUE
config_file["SECTION_NAME"]["KEY"]="VALUE"

# ADD A NEW FIELD UNDER A SECTION
config_file["SECTION_NAME"].update({"KEY":"(VALUE)"})

# DELETE A FIELD IN THE SECTION
config_file.remove_option('SECTION_NAME', 'KEY')

# DELETE A SECTION
config_file.remove_section('SECTION_NAME')

# SAVE THE SETTINGS TO THE FILE
with open("configurations.ini","w") as file_object:
    config_file.write(file_object)

# DISPLAY UPDATED SAVED SETTINGS
print("Config file 'configurations.ini' is updated")
print("Updated file settings are:\n")
file=open("configurations.ini","r")
settings=file.read()
print(settings)
    
    
    
"""
