from dataclasses import dataclass
from datetime import datetime

from pvlib.modelchain import ModelChainResult


@dataclass
class Position:
    latitude: float = None
    longitude: float = None
    altitude: float = None


@dataclass
class Roof:
    height: float = None
    azimuth: float = None
    tilt: float = None


@dataclass
class PV:
    number_of_modules: int = None
    azimuth: float = None
    tilt: float = None
    module: str = None
    case: str = None
    inverter: str = None


@dataclass
class SimulationTime:
    start: datetime = None
    end: datetime = None


@dataclass
class Result:
    output: ModelChainResult = None
    tilt: float = None
    azimuth: float = None
