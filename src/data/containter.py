from dataclasses import dataclass
from datetime import datetime

from pvlib.modelchain import ModelChainResult
from constants.enums import *
from constants.defaults import *

@dataclass
class Position:
    latitude: float = LATITUDE
    longitude: float = LONGITUDE
    altitude: float = ALTITUDE


@dataclass
class TimeWindow:
    start: datetime = TIME[0]
    end: datetime = TIME[1]


@dataclass
class PV:
    panel_manufacturer: str = PANEL_MANUFACTURER
    panel_series: str = PANEL_SERIES
    panel_model: str = PANEL_MODEL
    case: str = CASE
    number_of_modules: int = NUMBER_OF_MODULES
    bipartite: bool = BIPARTITE
    side1: int = NUMBER_OF_MODULES
    side2: int = 0
    opt_tilt: OptimizationState = OPT_TILT
    tilt: float = TILT
    min_tilt: float = 0
    max_tilt: float = 90
    opt_azimuth: OptimizationState = OPT_AZIMUTH
    azimuth: float = AZIMUTH
    min_azimuth: float = 0
    max_azimuth: float = 360
    inverter_manufacturer: str = INVERTER_MANUFACTURER
    inverter_series: str = INVERTER_SERIES
    inverter_model: str = INVERTER_MODEL


@dataclass
class Result:
    output: ModelChainResult = None
    tilt: float = None
    azimuth: float = None
