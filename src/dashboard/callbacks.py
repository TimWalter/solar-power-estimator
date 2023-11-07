from dash import Input, Output, State, no_update
from pvlib.location import Location

import data.disk_cached
from constants.ids import ids
from dashboard.figures import get_table_data, get_table_columns, get_graph_figure
from dashboard.figures import progress_figure, map_figure
from data.altitude_provider import altitude_provider
from data.containter import *
from data.ram_cached import ram_cache
from optimization import optimize
from simulation import simulate


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
        *([State(idx, "value") for idx in ids.input.pv.panel.stats]),
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
        *([State(idx, "value") for idx in ids.input.pv.inverter.stats]),
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
            v_mp,
            i_mp,
            v_oc,
            i_sc,
            t_v_oc,
            t_i_sc,
            t_p_mp,
            technology,
            n_cells_series,
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
            paco,
            pdco,
            vdco,
            pso,
            c0,
            c1,
            c2,
            c3,
            pnt,
            start_str,
            end_str,
    ):
        if n_clicks is None:
            return no_update, no_update

        pos = Location(latitude, longitude, altitude=altitude)
        time = DateTimeRange(
            datetime.strptime(start_str, "%Y-%m-%dT%H:%M:%S"),
            datetime.strptime(end_str, "%Y-%m-%dT%H:%M:%S"),
        )

        pv = PVSystemData(
            modules=[PVSystemData.Module(
                panel=PVSystemData.Module.Panel(
                    manufacturer=panel_manufacturer,
                    series=panel_series,
                    model=panel_model,
                    stats=PVSystemData.Module.Panel.Stats(
                        cell_type=CellType.from_cec(technology),
                        v_mp=v_mp,
                        i_mp=i_mp,
                        v_oc=v_oc,
                        i_sc=i_sc,
                        t_v_oc=t_v_oc,
                        t_i_sc=t_i_sc,
                        t_p_mp=t_p_mp,
                        n_cells_series=n_cells_series,
                    )
                ),
                case=Cases[case],
            )] * number_of_modules,
            bipartite=bipartite,
            side1=side1,
            side2=side2,
            tilt=tilt,
            azimuth=azimuth,
            inverter=PVSystemData.Inverter(
                manufacturer=inverter_manufacturer,
                series=inverter_series,
                model=inverter_model,
                stats=PVSystemData.Inverter.Stats(
                    p_aco=paco,
                    p_dco=pdco,
                    v_dco=vdco,
                    p_so=pso,
                    c0=c0,
                    c1=c1,
                    c2=c2,
                    c3=c3,
                    p_nt=pnt,
                ),
            )
        )

        tilt_info = OptimizableVariable(tilt, min_tilt, max_tilt, opt_tilt)
        azimuth_info = OptimizableVariable(azimuth, min_azimuth, max_azimuth, opt_azimuth)

        # Step 1: Fetch Data
        radiation = data.disk_cached.fetch_radiation(pos, time)
        set_progress(progress_figure(1))

        # Step 2: Optimization
        pv.tilt, pv.azimuth = optimize(pos, pv, radiation, tilt_info, azimuth_info)
        set_progress(progress_figure(2))

        # Step 3: Simulation
        result = simulate(pos, pv, radiation)
        set_progress(progress_figure(3))

        return (
            get_table_data(pv, result, tilt_info, azimuth_info),
            get_graph_figure(pv.bipartite, pv.side1, pv.side2, result),
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
    def synchronize_component(id_prefix, data, stats_keys):
        @app.callback(
            Output(id_prefix.series, "options"),
            Output(id_prefix.model, "options"),
            *([Output(idx, "value") for idx in id_prefix.stats]),
            Input(id_prefix.manufacturer, "value"),
            Input(id_prefix.series, "value"),
            Input(id_prefix.model, "value"),
            Input(id_prefix.custom.button, "active"),
            prevent_initial_callback=True,
        )
        def callback_synchronize_component(manufacturer, series, model, custom):
            if manufacturer is None or series is None or model is None:
                return (*([no_update] * (len(id_prefix.stats) + 2)),)

            try:
                series_options = list(data[manufacturer].keys())
            except KeyError:
                series_options = [] if not custom else [series]
            try:
                model_options = list(
                    data[manufacturer][series].keys()
                )
            except KeyError:
                model_options = [] if not custom else [model]
            try:
                stats = data[manufacturer][series][model]
                stats = [stats[key] for key in stats_keys]
            except KeyError:
                stats = [""] * len(stats_keys)

            return (
                series_options,
                model_options,
                *stats,
            )

    synchronize_component(ids.input.pv.panel, ram_cache.panels, PVSystemData.Module.Panel.Stats(*([None] * 9)).to_cec().keys())
    synchronize_component(ids.input.pv.inverter, ram_cache.inverters, PVSystemData.Inverter.Stats(*([None] * 9)).to_cec().keys())

    def get_dropdown_as_text_input(app, idx, idx_store, idx_button, duplicate=False):
        @app.callback(
            Output(idx, "options", allow_duplicate=duplicate),
            Output(idx_store, "data"),
            Input(idx, "search_value"),
            State(idx_store, "data"),
            State(idx, "options"),
            State(idx_button, "active"),
            prevent_initial_callback=True,
            prevent_initial_call="initial_duplicate" if duplicate else True,
        )
        def dropdown_as_text_input(query, previous_query, options, custom):
            if custom and query:
                if previous_query is None and len(query) > 0:  # started typing
                    if options:
                        options.insert(0, query)
                    else:
                        options = [query]
                elif len(query) > 0 and len(previous_query) > 0:  # continued typing
                    options[0] = query
                elif len(query) == 0:  # deleted all inputs
                    options = options[:-1]

                return options, query
            return no_update, no_update

    get_dropdown_as_text_input(app, ids.input.pv.panel.manufacturer, ids.input.pv.panel.custom.manufacturer_store,
                               ids.input.pv.panel.custom.button)
    get_dropdown_as_text_input(app, ids.input.pv.panel.series, ids.input.pv.panel.custom.series_store,
                               ids.input.pv.panel.custom.button, True)
    get_dropdown_as_text_input(app, ids.input.pv.panel.model, ids.input.pv.panel.custom.model_store,
                               ids.input.pv.panel.custom.button, True)

    get_dropdown_as_text_input(app, ids.input.pv.inverter.manufacturer,
                               ids.input.pv.inverter.custom.manufacturer_store,
                               ids.input.pv.inverter.custom.button)
    get_dropdown_as_text_input(app, ids.input.pv.inverter.series, ids.input.pv.inverter.custom.series_store,
                               ids.input.pv.inverter.custom.button, True)
    get_dropdown_as_text_input(app, ids.input.pv.inverter.model, ids.input.pv.inverter.custom.model_store,
                               ids.input.pv.inverter.custom.button, True)

    def get_toggle_button_callback(app, idx):
        @app.callback(
            Output(idx, "active"),
            Input(idx, "n_clicks"),
            State(idx, "active"),
            prevent_initial_callback=True,
        )
        def toggle(n_clicks, active):
            if not n_clicks:
                return no_update
            return not active

    get_toggle_button_callback(app, ids.input.pv.panel.custom.button)
    get_toggle_button_callback(app, ids.input.pv.inverter.custom.button)
    get_toggle_button_callback(app, ids.input.pv.bipartite.button)

    def custom_button_callback(app, idx_prefix):
        @app.callback(
            Output(idx_prefix.stats.accordion, "active_item"),
            Output(idx_prefix.custom.fade, "is_in"),
            Output(idx_prefix.custom.save, "disabled"),
            *([Output(idx, "disabled") for idx in idx_prefix.stats]),
            Input(idx_prefix.custom.button, "active"),
            prevent_initial_callback=True,
        )
        def custom_button(active):
            if active:
                return ["item-0"], True, *([False] * (1 + len(idx_prefix.stats)))
            else:
                return no_update, False, *([True] * (1 + len(idx_prefix.stats)))

    custom_button_callback(app, ids.input.pv.panel)
    custom_button_callback(app, ids.input.pv.inverter)

    def get_save_button_callback(app, idx_prefix, save_func):
        @app.callback(
            Output(idx_prefix.custom.success, "is_open"),
            Input(idx_prefix.custom.save, "n_clicks"),
            State(idx_prefix.manufacturer, "value"),
            State(idx_prefix.series, "value"),
            State(idx_prefix.model, "value"),
            *([State(idx, "value") for idx in idx_prefix.stats]),
            prevent_initial_callback=True,
        )
        def save_custom_panel(
                n_clicks,
                manufacturer,
                series,
                model,
                *stats,
        ):
            if n_clicks is None:
                return no_update
            save_func(manufacturer, series, model, *stats)
            return True

    get_save_button_callback(app, ids.input.pv.panel, ram_cache.save_panel)
    get_save_button_callback(app, ids.input.pv.inverter, ram_cache.save_inverter)

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
        State(ids.input.pv.bipartite.side1, "value"),
        State(ids.input.pv.bipartite.side2, "value"),
        prevent_initial_call="initial_duplicate",
    )
    def adapt_outputs(tilt_optimization_state, azimuth_optimization_state, bipartite, side1, side2):
        return get_table_columns(
            OptimizationState(tilt_optimization_state),
            OptimizationState(azimuth_optimization_state),
            bipartite
        ), get_graph_figure(bipartite,
                            side1,
                            side2)
