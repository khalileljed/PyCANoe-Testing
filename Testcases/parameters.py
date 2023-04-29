import ast
import configparser
import helper

def read_config():
    # Method to read config file settings

    config = configparser.ConfigParser()
    # full path here
    # config.read('C:/Users/ilyes/Desktop/AOLOA-Projects/PyCANoe-Testing/Examples/pytest/configurations.ini')
    config.read(
        'C:/Projects/PyCANoe-Testing/Testcases/configurations.ini')
    return config
# Parameters
config = read_config()

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
DM_sport_ind = int(config['Drivemodes']['dm_sport_ind'])
DM_offroad_ind = int(config['Drivemodes']['dm_offroad_ind'])
DM_sportplus_ind = int(config['Drivemodes']['dm_sportplus_ind'])

# Signals
AERO_SETUP = ast.literal_eval(config['Signals']['aero_setup'])
ACTUAL_POS = ast.literal_eval(config['Signals']['actual_pos'])
ACTUAL_Drehrichtung = ast.literal_eval(
    config['Signals']['actual_drehrichtung'])
Spoi_Initialisiert = ast.literal_eval(config['Signals']['spoi_initialisiert'])
Spoi_Referenziert = ast.literal_eval(config['Signals']['spoi_referenziert'])
Spoi_Pos_erreicht = ast.literal_eval(config['Signals']['spoi_pos_erreicht'])
Soll_Pos = ast.literal_eval(config['Signals']['soll_pos'])
Freigabe_Verst = ast.literal_eval(config['Signals']['freigabe_verst'])
Anf_Referenzierung = ast.literal_eval(config['Signals']['anf_referenzierung'])
ACTUAL_SPEED = ast.literal_eval(config['Signals']['actual_speed'])
LAUNCH = ast.literal_eval(config['Signals']['launch'])
DriveMode = ast.literal_eval(config['Signals']['drivemode'])
AERO_1_ERROR = ast.literal_eval(config['Signals']['aero_1_error'])
CHA_PROFCHNGD = ast.literal_eval(config['Signals']['cha_profchngd'])
AERO_REQ_SKE = ast.literal_eval(config['Signals']['aero_req_ske'])
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
Vthresh_SAD_Setup0to1 = float(config['SAD']['vthresh_sad_setup0to1'])
Vthresh_SAD_Setup1to2 = float(config['SAD']['vthresh_sad_setup1to2'])
Vthresh_SAD_Setup2to1 = float(config['SAD']['vthresh_sad_setup2to1'])
Vthresh_SAD_Setup1to0 = float(config['SAD']['vthresh_sad_setup1to0'])
vmax = float(config['SAD']['vmax'])

# MAN_SETUP
vthresh_man_setup1to2 = float(config['MAN_SETUP']['vthresh_man_setup1to2'])
vthresh_man_setup2to3 = float(config['MAN_SETUP']['vthresh_man_setup2to3'])
vthresh_man_setup3to2 = float(config['MAN_SETUP']['vthresh_man_setup3to2'])
vthresh_man_setup2to1 = float(config['MAN_SETUP']['vthresh_man_setup2to1'])

# Coding parameters
vMaxFahrProg = float(config['Coding parameters']['vmaxfahrprog'])
vTippTast = float(config['Coding parameters']['vtipptast'])
vMaxManMod = float(config['Coding parameters']['vmaxmanmod'])
vFzgManModSperrungInaktiv = float(config['Coding parameters']['vfzgmanmodsperrunginaktiv'])

# AERO_SETUP Values
MAN_SETUP_1 = float(config['AERO_SETUP Values']['man_setup_1'])
MAN_SETUP_2 = float(config['AERO_SETUP Values']['man_setup_2'])
MAN_SETUP_3 = float(config['AERO_SETUP Values']['man_setup_3'])
MAN_SETUP_4 = float(config['AERO_SETUP Values']['man_setup_4'])
