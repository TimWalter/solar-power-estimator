from dataclasses import dataclass, field
from datetime import datetime

from constants.enums import *

@dataclass
class Defaults:
    @dataclass
    class Location:
        name: str = "Weißenbach Sarntal"
        latitude: float = 46.77036973837921
        longitude: float = 11.372327644143732
        altitude: float = 1330

    location: Location = field(default_factory=Location)

    @dataclass
    class DateTimeRange:
        start: datetime = datetime(2020, 1, 1, 0, 0, 0)
        end: datetime = datetime(2020, 12, 31, 0, 0, 0)

    datetime_range: DateTimeRange = field(default_factory=DateTimeRange)

    @dataclass
    class PV:
        @dataclass
        class Module:
            @dataclass
            class Panel:
                manufacturer: str = "SunPower SPR"
                series: str = "X22"
                model: str = "360"

            panel: Panel = field(default_factory=Panel)
            case: Cases = Cases.CloseMountGlassGlass
            tilt: float = 30
            azimuth: float = 30

        module: Module = field(default_factory=Module)
        number_of_modules: int = 2
        bipartite: bool = False
        side1: int = 2
        side2: int = 0

        @dataclass
        class Inverter:
            manufacturer: str = "SMA America US"
            series: str = "SB10000TL"
            model: str = "208V"

        inverter: Inverter = field(default_factory=Inverter)

    pv: PV = field(default_factory=PV)


defaults = Defaults()
