from dash import Input, Output, State, no_update

from data.altitude_provider import altitude_provider
from dashboard.figures import progress_figure, map_figure
from simulation import simulate
from optimization import optimize
from dashboard.figures import get_table_data, get_table_columns, get_graph_figure
from constants.ids import ids
from constants.enums import *
from data.containter import *

import data.disk_cached
import data.ram_cached


def get_callbacks(app):
    get_input_callbacks(app)
    get_output_callbacks(app)

    @app.callback(
        Output(ids.output.table, "data"),
        Output(ids.output.graph, "figure"),
        Input(ids.control.start, "n_clicks"),
        State(ids.input.location.latitude, "value"),
        State(ids.input.location.longitude, "value"),
        State(ids.input.location.altitude, "value"),
        State(ids.input.pv.panel.manufacturer, "value"),
        State(ids.input.pv.panel.series, "value"),
        State(ids.input.pv.panel.model, "value"),
        State(ids.input.pv.case, "value"),
        State(ids.input.pv.number_of_modules, "value"),
        State(ids.input.pv.bipartite.button, "active"),
        State(ids.input.pv.bipartite.side1, "value"),
        State(ids.input.pv.bipartite.side2, "value"),
        State(ids.input.pv.tilt.radio, "value"),
        State(ids.input.pv.tilt.fix.input, "value"),
        State(ids.input.pv.tilt.constrain.min, "value"),
        State(ids.input.pv.tilt.constrain.max, "value"),
        State(ids.input.pv.azimuth.radio, "value"),
        State(ids.input.pv.azimuth.fix.input, "value"),
        State(ids.input.pv.azimuth.constrain.min, "value"),
        State(ids.input.pv.azimuth.constrain.max, "value"),
        State(ids.input.pv.inverter.manufacturer, "value"),
        State(ids.input.pv.inverter.series, "value"),
        State(ids.input.pv.inverter.model, "value"),
        State(ids.input.time, "start_date"),
        State(ids.input.time, "end_date"),
        background=True,
        running=[
            (Output(ids.control.start, "disabled"), True, False),
            (Output(ids.control.cancel.button, "disabled"), False, True),
            (Output(ids.control.cancel.fade, "is_in"), True, False),
            (Output(ids.control.loading.gif, "hidden"), False, True),
            (Output(ids.control.loading.placeholder, "hidden"), True, False),
        ],
        cancel=[Input(ids.control.cancel.button, "n_clicks")],
        progress=Output(ids.control.progress_bar, "figure"),
        progress_default=progress_figure(0),
        prevent_initial_callback=True,
    )
    def start_simulation(
        set_progress,
        n_clicks,
        latitude,
        longitude,
        altitude,
        panel_manufacturer,
        panel_series,
        panel_model,
        case,
        number_of_modules,
        bipartite,
        side1,
        side2,
        opt_tilt,
        tilt,
        min_tilt,
        max_tilt,
        opt_azimuth,
        azimuth,
        min_azimuth,
        max_azimuth,
        inverter_manufacturer,
        inverter_series,
        inverter_model,
        start_str,
        end_str,
    ):
        if n_clicks is None:
            return no_update, no_update

        pos = Position(latitude, longitude, altitude)
        pv = PV(
            panel_manufacturer,
            panel_series,
            panel_model,
            case,
            number_of_modules,
            bipartite,
            side1,
            side2,
            opt_tilt,
            tilt,
            min_tilt,
            max_tilt,
            opt_azimuth,
            azimuth,
            min_azimuth,
            max_azimuth,
            inverter_manufacturer,
            inverter_series,
            inverter_model,
        )
        time = TimeWindow(
            datetime.strptime(start_str, "%Y-%m-%dT%H:%M:%S"),
            datetime.strptime(end_str, "%Y-%m-%dT%H:%M:%S"),
        )

        # Step 1: Fetch Data
        radiation = data.disk_cached.fetch_radiation(pos, time)
        set_progress(progress_figure(1))

        # Step 2: Optimization
        pv.tilt, pv.azimuth = optimize(pos, pv, radiation)
        set_progress(progress_figure(2))

        # Step 3: Simulation
        result = simulate(pos, pv, radiation)
        set_progress(progress_figure(3))

        return (
            get_table_data(pv, result),
            get_graph_figure(pv, result),
        )


def get_input_callbacks(app):
    get_location_callbacks(app)
    get_pv_callbacks(app)


def get_location_callbacks(app):
    @app.callback(
        Output(ids.input.location.name, "options"),
        Input(ids.input.location.name, "search_value"),
        prevent_initial_callback=True,
    )
    def update_location_options(search_value):
        return (
            [
                location["place_name"]
                for location in data.disk_cached.fetch_location(search_value)
            ]
            if search_value
            else no_update
        )

    @app.callback(
        Output(ids.input.location.latitude, "value"),
        Output(ids.input.location.longitude, "value"),
        Output(ids.input.location.altitude, "value"),
        Output(ids.input.location.map, "figure"),
        Input(ids.input.location.name, "value"),
        prevent_initial_callback=True,
    )
    def update_location_parameters(value):
        longitude, latitude = data.disk_cached.fetch_location(value)[0]["center"]
        altitude = altitude_provider.get_altitude(latitude, longitude)

        return (
            latitude,
            longitude,
            altitude,
            map_figure(latitude, longitude),
        )


def get_pv_callbacks(app):

    def get_manufacturer_series_model_callback(app, idx, data):
        @app.callback(
            Output(idx.series, "options"),
            Output(idx.model, "options"),
            Input(idx.manufacturer, "search_value"),
            Input(idx.series, "search_value"),
        )
        def update_options(manufacturer, series):
            if manufacturer is None or series is None:
                return no_update, no_update
            return data[manufacturer].keys(), data[manufacturer][series].keys()

    get_manufacturer_series_model_callback(app, ids.input.pv.panel, data.ram_cached.fetch_modules())
    get_manufacturer_series_model_callback(app, ids.input.pv.inverter, data.ram_cached.fetch_inverters())

    @app.callback(
        Output(ids.input.pv.bipartite.side1, "value"),
        Output(ids.input.pv.bipartite.side2, "value"),
        Input(ids.input.pv.number_of_modules, "value"),
    )
    def update_sides_from_number_of_modules(value):
        return value, 0

    @app.callback(
        Output(ids.input.pv.bipartite.side2, "value", allow_duplicate=True),
        Input(ids.input.pv.bipartite.side1, "value"),
        State(ids.input.pv.number_of_modules, "value"),
        prevent_initial_call="initial_duplicate",
    )
    def update_side2_from_side1(side1, number_of_modules):
        return number_of_modules - side1

    def get_optimizable_input_callback(app, idx):
        @app.callback(
            Output(idx.fix.collapse, "is_open"),
            Output(idx.constrain.collapse, "is_open"),
            Input(idx.radio, "value"),
        )
        def tilt_radio_inputs(value):
            return (
                value == OptimizationState.Fix.value,
                value == OptimizationState.Constrain.value,
            )

    get_optimizable_input_callback(app, ids.input.pv.tilt)
    get_optimizable_input_callback(app, ids.input.pv.azimuth)

    @app.callback(
        Output(ids.input.pv.bipartite.button, "active"),
        Input(ids.input.pv.bipartite.button, "n_clicks"),
        State(ids.input.pv.bipartite.button, "active"),
        prevent_initial_callback=True,
    )
    def toggle_bipartite(n_clicks, active):
        if not n_clicks:
            return no_update
        return not active

    @app.callback(
        Output(ids.input.pv.bipartite.collapse, "is_open"),
        Input(ids.input.pv.bipartite.button, "active"),
        prevent_initial_callback=True,
    )
    def collapse_distribution(active):
        return active


def get_output_callbacks(app):
    @app.callback(
        Output(ids.output.table, "columns"),
        Output(ids.output.graph, "figure", allow_duplicate=True),
        Input(ids.input.pv.tilt.radio, "value"),
        Input(ids.input.pv.azimuth.radio, "value"),
        Input(ids.input.pv.bipartite.button, "active"),
        prevent_initial_call="initial_duplicate",
    )
    def adapt_outputs(tilt_optimization_state, azimuth_optimization_state, bipartite):
        pv = PV()
        pv.opt_tilt = OptimizationState(tilt_optimization_state)
        pv.opt_azimuth = OptimizationState(azimuth_optimization_state)
        pv.bipartite = bipartite
        return get_table_columns(pv), get_graph_figure(pv)
