from dataclasses import dataclass, field
from datetime import datetime

from pvlib.modelchain import ModelChainResult

from constants import defaults as defaults


class DataclassSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        cls._instances[cls] = super(DataclassSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


@dataclass
class Results(metaclass=DataclassSingleton):
    result: ModelChainResult = None
    tilt: float = None
    azimuth: float = None


@dataclass
class State(metaclass=DataclassSingleton):
    latitude: float = defaults.LATITUDE
    longitude: float = defaults.LONGITUDE
    altitude: float = defaults.ALTITUDE
    panel_azimuth: float = defaults.PANEL_AZIMUTH
    panel_tilt: float = defaults.PANEL_ELEVATION
    house_height: float = defaults.HOUSE_HEIGHT
    start_time: datetime = defaults.TIME[0]
    end_time: datetime = defaults.TIME[1]
    roof_tilt: float = defaults.ROOF_TILT
    module: str = defaults.MODULE
    number_of_modules: int = defaults.NUMBER_OF_MODULES
    case: str = defaults.CASE
    inverter: str = defaults.INVERTER
    manual: Results = field(default_factory=Results)
    opt_one_sided: Results = field(default_factory=Results)
    opt_two_sided: Results = field(default_factory=Results)

    def __post_init__(self):
        """Type consistency checks"""
        if type(self.start_time) is str:
            self.start_time = datetime.strptime(self.start_time, "%Y-%m-%dT%H:%M:%S")
        if type(self.end_time) is str:
            self.end_time = datetime.strptime(self.end_time, "%Y-%m-%dT%H:%M:%S")


state = State()
