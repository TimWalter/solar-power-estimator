from dataclasses import dataclass
from datetime import datetime

from pvlib.modelchain import ModelChainResult

from constants.enums import CellType, Cases, OptimizationState


@dataclass
class DateTimeRange:
    start: datetime
    end: datetime


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
            @dataclass
            class Stats:
                cell_type: CellType
                v_mp: float
                i_mp: float
                v_oc: float
                i_sc: float
                t_i_sc: float
                t_v_oc: float
                t_p_mp: float
                n_cells_series: int

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

            stats: Stats

        panel: Panel
        case: Cases

    modules: list

    bipartite: bool
    side1: int
    side2: int
    tilt: float
    azimuth: float

    @dataclass
    class Inverter(ProductIdentifier):
        @dataclass
        class Stats:
            p_aco: float
            p_dco: float
            v_dco: float
            p_so: float
            c0: float
            c1: float
            c2: float
            c3: float
            p_nt: float

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

        stats: Stats

    inverter: Inverter


@dataclass
class Result:
    output: ModelChainResult
    tilt: float
    azimuth: float
