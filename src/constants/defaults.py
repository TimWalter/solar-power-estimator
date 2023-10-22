from datetime import datetime
from constants.enums import *

# Location
LOCATION = "Weißenbach Sarntal"
LATITUDE = 46.77036973837921
LONGITUDE = 11.372327644143732
ALTITUDE = 1330

# PV
PANEL_MANUFACTURER = "SunPower SPR"
PANEL_SERIES = "X22"
PANEL_MODEL = "360"
CASE = "close_mount_glass_glass"
NUMBER_OF_MODULES = 2
INVERTER_MANUFACTURER = "SMA America US"
INVERTER_SERIES = "SB10000TL"
INVERTER_MODEL = "208V"
BIPARTITE = False
DISTRIBUTION = NUMBER_OF_MODULES
OPT_TILT = OptimizationState.Fix
TILT = 30
OPT_AZIMUTH = OptimizationState.Fix
AZIMUTH = 30

# Time
TIME = [datetime(2020, 1, 1, 0, 0, 0), datetime(2020, 12, 31, 0, 0, 0)]
