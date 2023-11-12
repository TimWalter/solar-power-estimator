from enum import Enum


class OptimizationState(Enum):
    Fix = 0
    Optimize = 1
    Constrain = 2


class CellType(Enum):
    MonoSi = "monoSi"
    MultiSi = "multiSi"
    PolySi = "polySi"
    Cis = "cis"
    Cigs = "cigs"
    CdTe = "cdte"
    Amorphous = "amorphous"

    def to_cec(self) -> str:
        name = self.name
        if name == "MonoSi":
            name = "Mono-c-Si"
        elif name == "MultiSi":
            name = "Multi-c-Si"
        return name

    @staticmethod
    def from_cec(cec_name: str) -> "CellType":
        if cec_name == "Mono-c-Si":
            return CellType.MonoSi
        elif cec_name == "Multi-c-Si":
            return CellType.MultiSi
        else:
            return CellType[cec_name]


class Case(Enum):
    OpenRackGlassGlass = "open_rack_glass_glass"
    OpenRackGlassPolymer = "open_rack_glass_polymer"
    CloseMountGlassGlass = "close_mount_glass_glass"
    InsulatedBackGlassPolymer = "insulated_back_glass_polymer"
