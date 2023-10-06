import os
from dash import CeleryManager, DiskcacheManager, Input, Output, State, no_update

from data.altitude_provider import altitude_provider
from dashboard.figures import progress_figure, map_figure
from simulation import simulate
from optimization import optimize
from dashboard.figures import get_table_data, fig1, fig2, fig3
from constants.ids import *
from data.containter import *

import data.disk_cached
import data.ram_cached


def get_background_callback_manager():
    if "REDIS_URL" in os.environ:
        # Use Redis & Celery if REDIS_URL set as an env variable
        from celery import Celery

        celery_app = Celery(
            __name__, broker=os.environ["REDIS_URL"], backend=os.environ["REDIS_URL"]
        )
        return CeleryManager(celery_app)
    else:
        # Diskcache for non-production apps when developing locally
        import diskcache

        cache = diskcache.Cache("./cache")
        return DiskcacheManager(cache)


def get_callbacks(app):
    @app.callback(
        Output(MODULE_ID, "options"),
        Input(MODULE_ID, "search_value"),
        prevent_initial_callback=True,
    )
    def update_location_options(search_value):
        # Callback to show the modules found given the input query
        return (
            [o for o in data.ram_cached.fetch_modules().keys() if search_value in o]
            if search_value
            else no_update
        )

    @app.callback(
        Output(LOCATION_NAME_ID, "options"),
        Input(LOCATION_NAME_ID, "search_value"),
        prevent_initial_callback=True,
    )
    def search_location_name(search_value):
        # Callback to show the locations found given the input query
        return (
            [
                location["place_name"]
                for location in data.disk_cached.fetch_location(search_value)
            ]
            if search_value
            else no_update
        )

    @app.callback(
        Output(LATITUDE_ID, "value"),
        Output(LONGITUDE_ID, "value"),
        Output(ALTITUDE_ID, "value"),
        Output(MAP_ID, "figure"),
        Input(LOCATION_NAME_ID, "value"),
        prevent_initial_callback=True,
    )
    def update_location_parameters(value):
        # Callback to update the location parameters given the location name
        longitude, latitude = data.disk_cached.fetch_location(value)[0]["center"]
        altitude = altitude_provider.get_altitude(latitude, longitude)

        return (
            latitude,
            longitude,
            altitude,
            map_figure(Position(latitude, longitude, altitude)),
        )

    @app.callback(
        Output(OUTPUT_TABLE_ID, "data"),
        Output(OUTPUT_GRAPH_1_ID, "figure"),
        Output(OUTPUT_GRAPH_2_ID, "figure"),
        Output(OUTPUT_GRAPH_3_ID, "figure"),
        Input(START_BUTTON_ID, "n_clicks"),
        State(LATITUDE_ID, "value"),
        State(LONGITUDE_ID, "value"),
        State(ALTITUDE_ID, "value"),
        State(ROOF_HEIGHT_ID, "value"),
        State(ROOF_AZIMUTH_ID, "value"),
        State(ROOF_TILT_ID, "value"),
        State(NUMBER_OF_MODULES_ID, "value"),
        State(PANEL_AZIMUTH_ID, "value"),
        State(PANEL_TILT_ID, "value"),
        State(MODULE_ID, "value"),
        State(CASE_ID, "value"),
        State(INVERTER_ID, "value"),
        State(TIME_ID, "start_date"),
        State(TIME_ID, "end_date"),
        background=True,
        running=[
            (Output(START_BUTTON_ID, "disabled"), True, False),
            (Output(CANCEL_BUTTON_ID, "disabled"), False, True),
            (Output(LOADING_ICON_ID, "hidden"), False, True),
            (Output(NON_LOADING_ID, "hidden"), True, False),
        ],
        cancel=[Input(CANCEL_BUTTON_ID, "n_clicks")],
        progress=Output(PROGRESS_BAR_ID, "figure"),
        progress_default=progress_figure(0),
        prevent_initial_callback=True,
    )
    def start_simulation(
        set_progress,
        n_clicks,
        latitude,
        longitude,
        altitude,
        roof_height,
        roof_azimuth,
        roof_tilt,
        number_of_modules,
        panel_azimuth,
        panel_tilt,
        module,
        case,
        inverter,
        start_str,
        end_str,
    ):
        if n_clicks is None:
            return no_update, no_update, no_update, no_update

        pos = Position(latitude, longitude, altitude)
        roof = Roof(roof_height, roof_azimuth, roof_tilt)
        pv = PV(number_of_modules, panel_azimuth, panel_tilt, module, case, inverter)
        time = SimulationTime(
            datetime.strptime(start_str, "%Y-%m-%dT%H:%M:%S"),
            datetime.strptime(end_str, "%Y-%m-%dT%H:%M:%S"),
        )

        # Step 1: Fetch Data
        radiation = data.disk_cached.fetch_radiation(pos, time)
        set_progress(progress_figure(1))

        # Step 2: Simulate Manual
        result = simulate(pos, roof, pv, radiation)
        set_progress(progress_figure(2))

        # Step 3: 1. Optimization
        pv.azimuth, pv.tilt = optimize(pos, roof, pv, radiation, False)
        result_1s = simulate(pos, roof, pv, radiation, False)
        set_progress(progress_figure(3))

        # Step 4: 1. Optimization
        pv.azimuth, pv.tilt = optimize(pos, roof, pv, radiation, True)
        result_2s = simulate(pos, roof, pv, radiation, True)
        set_progress(progress_figure(4))

        return (
            get_table_data(result, result_1s, result_2s),
            fig1(result),
            fig2(result, result_1s, result_2s),
            fig3(result, result_1s, result_2s),
        )
