from dataclasses import dataclass, field
from datetime import datetime

import pvlib.location
from pvlib.modelchain import ModelChainResult

from constants.enums import CellType, Cases, OptimizationState
from data.ram_cached import ram_cache


class Location(pvlib.location.Location):
    def __init__(
        self,
        name: str = "Weißenbach Sarntal",
        latitude: float = 46.77036973837921,
        longitude: float = 11.372327644143732,
        altitude: float = 1330,
        **kwargs
    ):
        super().__init__(latitude, longitude, altitude=altitude, name=name, **kwargs)


@dataclass
class DateTimeRange:
    start: datetime = datetime(2020, 1, 1, 0, 0, 0)
    end: datetime = datetime(2020, 12, 31, 0, 0, 0)


@dataclass
class OptimizableVariable:
    value: float
    min: float
    max: float
    state: OptimizationState


@dataclass
class ProductIdentifier:
    manufacturer: str
    series: str
    model: str


@dataclass
class PVSystemData:
    @dataclass
    class Module:
        @dataclass
        class Panel(ProductIdentifier):
            manufacturer: str = "SunPower SPR"
            series: str = "X22"
            model: str = "360"

            @dataclass
            class Stats:
                cell_type: CellType = None
                v_mp: float = None
                i_mp: float = None
                v_oc: float = None
                i_sc: float = None
                t_i_sc: float = None
                t_v_oc: float = None
                t_p_mp: float = None
                n_cells_series: int = None

                def to_cec(self) -> dict:
                    return {
                        "V_mp_ref": self.v_mp,
                        "I_mp_ref": self.i_mp,
                        "V_oc_ref": self.v_oc,
                        "I_sc_ref": self.i_sc,
                        "alpha_sc": self.t_v_oc,
                        "beta_oc": self.t_i_sc,
                        "gamma_r": self.t_p_mp,
                        "Technology": self.cell_type.to_cec(),
                        "N_s": self.n_cells_series,
                    }

                @staticmethod
                def from_cec(data: dict):
                    self = PVSystemData.Module.Panel.Stats()
                    self.cell_type = CellType.from_cec(data["Technology"])
                    self.v_mp = data["V_mp_ref"]
                    self.i_mp = data["I_mp_ref"]
                    self.v_oc = data["V_oc_ref"]
                    self.i_sc = data["I_sc_ref"]
                    self.t_v_oc = data["alpha_sc"]
                    self.t_i_sc = data["beta_oc"]
                    self.t_p_mp = data["gamma_r"]
                    self.n_cells_series = data["N_s"]

            stats: Stats = field(
                default_factory=lambda: PVSystemData.Module.Panel.Stats.from_cec(
                    ram_cache.panels["SunPower SPR"]["X22"]["360"]
                )
            )

        panel: Panel = field(default_factory=Panel)
        case: Cases = Cases.CloseMountGlassGlass
        tilt: float = 30
        azimuth: float = 30

    modules: list = field(
        default_factory=lambda: [PVSystemData.Module(), PVSystemData.Module()]
    )
    bipartite: bool = False
    side1: int = 2
    side2: int = 0

    @dataclass
    class Inverter(ProductIdentifier):
        manufacturer: str = "SMA America US"
        series: str = "SB10000TL"
        model: str = "208V"

        @dataclass
        class Stats:
            p_aco: float = None
            p_dco: float = None
            v_dco: float = None
            p_so: float = None
            c0: float = None
            c1: float = None
            c2: float = None
            c3: float = None
            p_nt: float = None

            def to_cec(self) -> dict:
                return {
                    "Paco": self.p_aco,
                    "Pdco": self.p_dco,
                    "Vdco": self.v_dco,
                    "Pso": self.p_so,
                    "C0": self.c0,
                    "C1": self.c1,
                    "C2": self.c2,
                    "C3": self.c3,
                    "Pnt": self.p_nt,
                }

            @staticmethod
            def from_cec(data: dict):
                self = PVSystemData.Inverter.Stats()
                self.p_aco = data["Paco"]
                self.p_dco = data["Pdco"]
                self.v_dco = data["Vdco"]
                self.p_so = data["Pso"]
                self.c0 = data["C0"]
                self.c1 = data["C1"]
                self.c2 = data["C2"]
                self.c3 = data["C3"]
                self.p_nt = data["Pnt"]
                return self

        stats: Stats = field(
            default_factory=lambda: PVSystemData.Inverter.Stats.from_cec(
                ram_cache.inverters["SMA America US"]["SB10000TL"]["208V"]
            )
        )

    inverter: Inverter = field(default_factory=Inverter)


@dataclass
class Result:
    output: ModelChainResult
    tilt: float
    azimuth: float
