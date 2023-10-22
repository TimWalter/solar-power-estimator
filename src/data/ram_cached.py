import json
from dataclasses import dataclass


@dataclass
class RAMCache:
    modules: dict = None
    inverter: dict = None


ram_cache = RAMCache()


def fetch_modules() -> dict:
    if ram_cache.modules is None:
        with open("data/panel_database.json", "r") as file:
            ram_cache.modules = json.load(file)
    return ram_cache.modules


def fetch_inverters() -> dict:
    if ram_cache.inverter is None:
        with open("data/inverter_database.json", "r") as file:
            ram_cache.inverter = json.load(file)
    return ram_cache.inverter
