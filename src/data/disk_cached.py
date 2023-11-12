import io
import json

import pandas as pd
import requests
from joblib import Memory
from pvlib.location import Location

from constants.containter import DateTimeRange
from sec.keys import MAPTILER_API_KEY

memory = Memory("cache", verbose=0)


@memory.cache
def fetch_location(query: str) -> list:
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
def fetch_radiation(pos: Location, time: DateTimeRange) -> pd.Series:
    endpoint = "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc"
    params = {
        "lat": pos.latitude,
        "lon": pos.longitude,
        "startyear": time.start.year,
        "endyear": time.end.year,
        "components": "1",
        "outputformat": "csv",
    }

    response_h = requests.get(endpoint, params=params)
    params["trackingtype"] = 2
    response_n = requests.get(endpoint, params=params)

    if response_h.status_code == 200 and response_n.status_code == 200:
        data_h = pd.read_csv(
            io.StringIO(response_h.content.decode("utf-8")),
            skiprows=8,
            skipfooter=11,
            engine="python",
        )
        data_n = pd.read_csv(
            io.StringIO(response_n.content.decode("utf-8")),
            skiprows=8,
            skipfooter=11,
            engine="python",
        )
        radiation = pd.DataFrame(
            {
                "time": data_h["time"],
                "dni": data_n["Gb(i)"],
                "ghi": data_h["Gb(i)"] + data_h["Gd(i)"] + data_h["Gr(i)"],
                "dhi": data_h["Gd(i)"],
                "temp_air": data_h["T2m"],
                "wind_speed": data_h["WS10m"],
            }
        )
        radiation["time"] = pd.to_datetime(radiation["time"], format="%Y%m%d:%H%M")
        radiation = radiation[(radiation["time"] >= time.start) & (radiation["time"] <= time.end)]
        radiation.set_index("time", inplace=True)

        return radiation
    else:
        print(
            f"Failed to retrieve constants. Status code: {response_h.status_code}|{response_n.status_code}"
        )
        return pd.Series()
