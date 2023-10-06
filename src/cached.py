import io
import json
import pvlib
import requests
import pandas as pd
from joblib import Memory
from dataclasses import dataclass, field

from sec.keys import MAPTILER_API_KEY

import current


memory = Memory("cache", verbose=0)


@memory.cache
def fetch_geocoding(query: str) -> list:
    response = requests.get(
        f"https://api.maptiler.com/geocoding/{query}.json?key={MAPTILER_API_KEY}"
    )
    if response.status_code == 200:
        return json.loads(response.content)["features"]
    else:
        # Handle the case when the request fails
        print(f"Failed to retrieve constants. Status code: {response.status_code}")
        return []


@memory.cache
def fetch_pvgis(latitude, longitude, start_year, end_year, normal: bool = False):
    endpoint = "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc"
    params = {
        "lat": latitude,
        "lon": longitude,
        "startyear": start_year,
        "endyear": end_year,
        "components": "1",
        "outputformat": "csv",
    }
    if normal:
        params["trackingtype"] = 2
    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        return pd.read_csv(
            io.StringIO(response.content.decode("utf-8")),
            skiprows=8,
            skipfooter=11,
            engine="python",
        )
    else:
        print(f"Failed to retrieve constants. Status code: {response.status_code}")
        return pd.Series()


@dataclass
class Data:
    modules: dict = None
    cases: dict = None
    inverter: dict = None
    radiation: pd.Series = field(default_factory=pd.Series)

    def __post_init__(self):
        self.cases = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS["sapm"]

    def fetch_modules(self) -> dict:
        if self.modules is None:
            self.modules = pvlib.pvsystem.retrieve_sam(
                "CECMod", path="../data/CEC Modules.csv"
            )
        return self.modules

    def fetch_inverters(self) -> dict:
        if self.inverter is None:
            self.inverter = pvlib.pvsystem.retrieve_sam(
                "CECinverter", path="../data/CEC Inverters.csv"
            )
        return self.inverter

    def fetch_locations(self, query: str) -> list:
        return [f["place_name"] for f in fetch_geocoding(query)]

    def fetch_coordinates(self, query: str):
        return fetch_geocoding(query)[0]["center"]

    def fetch_radiation(self) -> pd.Series:
        params = {
            current.state.latitude,
            current.state.longitude,
            current.state.start_time.year,
            current.state.end_time.year,
        }

        data_horizontal = fetch_pvgis(
            current.state.latitude,
            current.state.longitude,
            current.state.start_time.year,
            current.state.end_time.year,
        )
        data_normal = fetch_pvgis(
            current.state.latitude,
            current.state.longitude,
            current.state.start_time.year,
            current.state.end_time.year,
            normal=True
        )

        radiation = pd.DataFrame(
            {
                "time": data_horizontal["time"],
                "dni": data_normal["Gb(i)"],
                "ghi": data_horizontal["Gb(i)"]
                + data_horizontal["Gd(i)"]
                + data_horizontal["Gr(i)"],
                "dhi": data_horizontal["Gd(i)"],
                "temp_air": data_horizontal["T2m"],
                "wind_speed": data_horizontal["WS10m"],
            }
        )

        radiation["time"] = pd.to_datetime(radiation["time"], format="%Y%m%d:%H%M")
        radiation = radiation[
            (radiation["time"] >= current.state.start_time)
            & (radiation["time"] <= current.state.end_time)
        ]
        radiation.set_index("time", inplace=True)

        self.radiation = radiation
        return radiation

    def fetch_best_module(self) -> dict:
        best_key = ""
        best_stat = 0
        for key in self.fetch_modules():
            module = self.modules[key]
            stats = module["I_mp_ref"] * module["V_mp_ref"] / module["A_c"]
            if stats > best_stat and module["Technology"] == "Mono-c-Si":
                best_key = key
                best_stat = stats
        result = self.modules[best_key]
        result["name"] = best_key
        return result

    def fetch_fitting_inverter(self, module: dict, number_of_modules: int) -> dict:
        single_max_power = module["I_mp_ref"] * module["V_mp_ref"]
        for key in self.fetch_inverters():
            inverter = self.inverter[key]
            min_power_condition = inverter["Pso"] <= single_max_power
            max_power_condition = (
                inverter["Pdco"] >= single_max_power * number_of_modules
            )
            manufacturer_condition = "SMA" in key
            if min_power_condition and max_power_condition and manufacturer_condition:
                return inverter


data = Data()
