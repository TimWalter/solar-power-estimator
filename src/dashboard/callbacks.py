import os
from dash import CeleryManager, DiskcacheManager, Input, Output, State, no_update

from elevation_provider import elevation_provider
from dashboard.figures import progress_figure, map_figure
from simulation import simulate
from optimization import optimize
from dashboard.figures import get_table_data, fig1, fig2, fig3
from constants.ids import *

import current
import cached


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
            [o for o in cached.data.fetch_modules().keys() if search_value in o]
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
        return cached.data.fetch_locations(search_value) if search_value else no_update

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
        longitude, latitude = cached.data.fetch_coordinates(value)
        altitude = elevation_provider.get_elevation(latitude, longitude)

        current.state.latitude = latitude
        current.state.longitude = longitude
        current.state.altitude = altitude

        return latitude, longitude, altitude, map_figure()

    @app.callback(
        Output(OUTPUT_TABLE_ID, "data"),
        Output(OUTPUT_GRAPH_1_ID, "figure"),
        Output(OUTPUT_GRAPH_2_ID, "figure"),
        Output(OUTPUT_GRAPH_3_ID, "figure"),
        Input(START_BUTTON_ID, "n_clicks"),
        State(LATITUDE_ID, "value"),
        State(LONGITUDE_ID, "value"),
        State(ALTITUDE_ID, "value"),
        State(PANEL_AZIMUTH_ID, "value"),
        State(PANEL_ELEVATION_ID, "value"),
        State(HOUSE_HEIGHT_ID, "value"),
        State(TIME_ID, "start_date"),
        State(TIME_ID, "end_date"),
        State(ROOF_TILT_ID, "value"),
        State(MODULE_ID, "value"),
        State(NUMBER_OF_MODULES_ID, "value"),
        State(CASE_ID, "value"),
        State(INVERTER_ID, "value"),
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
        *simulation_parameters,
    ):
        if n_clicks is None:
            return no_update, no_update, no_update, no_update

        current.state = current.State(*simulation_parameters)

        # Step 1: Fetch Data
        cached.data.fetch_radiation()
        set_progress(progress_figure(1))

        # Step 2: Simulate Manual
        current.state.manual.result = simulate()
        current.state.manual.tilt = current.state.panel_tilt
        current.state.manual.azimuth = current.state.panel_azimuth
        set_progress(progress_figure(2))

        # Step 3: Optimize one-sided
        (
            current.state.opt_one_sided.tilt,
            current.state.opt_one_sided.azimuth,
        ) = optimize(False)
        set_progress(progress_figure(3))

        # Step 4: Simulate one-sided
        current.state.opt_one_sided.result = simulate()
        set_progress(progress_figure(4))

        # Step 5: Optimize two-sided
        (
            current.state.opt_two_sided.tilt,
            current.state.opt_two_sided.azimuth,
        ) = optimize(True)
        set_progress(progress_figure(5))

        # Step 6: Simulate two-sided
        current.state.opt_two_sided.result = simulate(True)
        set_progress(progress_figure(6))

        return get_table_data(), fig1(), fig2(), fig3()
