import pvlib
from dataclasses import dataclass


@dataclass
class RAMCache:
    modules: dict = None
    inverter: dict = None


ram_cache = RAMCache()


def fetch_modules() -> dict:
    if ram_cache.modules is None:
        ram_cache.modules = pvlib.pvsystem.retrieve_sam(
            "CECMod", path="../../data/CEC Modules.csv"
        )
    return ram_cache.modules


def fetch_inverters() -> dict:
    if ram_cache.inverter is None:
        ram_cache.inverter = pvlib.pvsystem.retrieve_sam(
            "CECinverter", path="../../data/CEC Inverters.csv"
        )
    return ram_cache.inverter
