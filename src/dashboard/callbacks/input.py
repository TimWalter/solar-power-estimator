from dataclasses import asdict

import dash
from dash import Input, Output, State, no_update

import data.disk_cached
from constants.containter import *
from constants.ids import ids
from dashboard.figures import map_figure
from data.altitude_provider import altitude_provider
from data.ram_cached import ram_cache


def no_import_removal():
    pass


@dash.callback(
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


@dash.callback(
    Output(ids.input.location.latitude, "value"),
    Output(ids.input.location.longitude, "value"),
    Output(ids.input.location.altitude, "value"),
    Output(ids.input.location.map, "figure"),
    Input(ids.input.location.name, "value"),
    prevent_initial_callback=True,
)
def update_location_parameters(name):
    longitude, latitude = data.disk_cached.fetch_location(name)[0]["center"]
    altitude = altitude_provider.get_altitude(latitude, longitude)

    return (
        latitude,
        longitude,
        altitude,
        map_figure(latitude, longitude),
    )


def synchronize_product_identifiers(id_prefix, data, stats_keys):
    @dash.callback(
        Output(id_prefix.series.input, "options"),
        Output(id_prefix.model.input, "options"),
        *([Output(idx, "value") for idx in list(asdict(id_prefix.stats).values())[1:]]),
        Input(id_prefix.manufacturer.input, "value"),
        Input(id_prefix.series.input, "value"),
        Input(id_prefix.model.input, "value"),
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
            model_options = list(data[manufacturer][series].keys())
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


synchronize_product_identifiers(
    ids.input.pv.panel,
    ram_cache.panels,
    PVSystemData.Module.Panel.Stats(*([None] * 9)).to_cec().keys(),
)
synchronize_product_identifiers(
    ids.input.pv.inverter,
    ram_cache.inverters,
    PVSystemData.Inverter.Stats(*([None] * 9)).to_cec().keys(),
)


def make_product_identifier_dropdown_text_input(id_prefix):
    def make_dropdown_text_input(idx_dropdown, idx_button, duplicate=False):
        @dash.callback(
            Output(idx_dropdown.input, "options", allow_duplicate=duplicate),
            Output(idx_dropdown.store, "data"),
            Input(idx_dropdown.input, "search_value"),
            State(idx_dropdown.store, "data"),
            State(idx_dropdown.input, "options"),
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

    make_dropdown_text_input(id_prefix.manufacturer, id_prefix.custom.button)
    make_dropdown_text_input(id_prefix.series, id_prefix.custom.button, True)
    make_dropdown_text_input(id_prefix.model, id_prefix.custom.button, True)


make_product_identifier_dropdown_text_input(ids.input.pv.panel)
make_product_identifier_dropdown_text_input(ids.input.pv.inverter)


def make_toggle_button(idx):
    @dash.callback(
        Output(idx, "active"),
        Input(idx, "n_clicks"),
        State(idx, "active"),
        prevent_initial_callback=True,
    )
    def toggle(n_clicks, active):
        if not n_clicks:
            return no_update
        return not active


make_toggle_button(ids.input.pv.panel.custom.button)
make_toggle_button(ids.input.pv.inverter.custom.button)
make_toggle_button(ids.input.pv.bipartite.button)


def custom_button_callback(idx_prefix):
    @dash.callback(
        Output(idx_prefix.stats.accordion, "active_item"),
        Output(idx_prefix.custom.fade, "is_in"),
        Output(idx_prefix.custom.save, "disabled"),
        *([Output(idx, "disabled") for idx in list(asdict(idx_prefix.stats).values())[1:]]),
        Input(idx_prefix.custom.button, "active"),
        prevent_initial_callback=True,
    )
    def custom_button(active):
        if active:
            return ["item-0"], True, *([False] * len(asdict(idx_prefix.stats).values()))
        else:
            return no_update, False, *([True] * len(asdict(idx_prefix.stats).values()))


custom_button_callback(ids.input.pv.panel)
custom_button_callback(ids.input.pv.inverter)


def save_button_callback(idx_prefix, save_func):
    @dash.callback(
        Output(idx_prefix.custom.success, "is_open"),
        Input(idx_prefix.custom.save, "n_clicks"),
        State(idx_prefix.manufacturer.input, "value"),
        State(idx_prefix.series.input, "value"),
        State(idx_prefix.model.input, "value"),
        *([State(idx, "value") for idx in list(asdict(idx_prefix.stats).values())[1:]]),
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


save_button_callback(ids.input.pv.panel, ram_cache.save_panel)
save_button_callback(ids.input.pv.inverter, ram_cache.save_inverter)


@dash.callback(
    Output(ids.input.pv.bipartite.side1, "value"),
    Output(ids.input.pv.bipartite.side2, "value"),
    Input(ids.input.pv.number_of_modules, "value"),
)
def update_sides_from_number_of_modules(value):
    return value, 0


@dash.callback(
    Output(ids.input.pv.bipartite.side2, "value", allow_duplicate=True),
    Input(ids.input.pv.bipartite.side1, "value"),
    State(ids.input.pv.number_of_modules, "value"),
    prevent_initial_call="initial_duplicate",
)
def update_side2_from_side1(side1, number_of_modules):
    return number_of_modules - side1


def get_optimizable_input_callback(idx):
    @dash.callback(
        Output(idx.fix.collapse, "is_open"),
        Output(idx.constrain.collapse, "is_open"),
        Input(idx.radio, "value"),
    )
    def tilt_radio_inputs(value):
        return (
            value == OptimizationState.Fix.value,
            value == OptimizationState.Constrain.value,
        )


get_optimizable_input_callback(ids.input.pv.tilt)
get_optimizable_input_callback(ids.input.pv.azimuth)


@dash.callback(
    Output(ids.input.pv.bipartite.collapse, "is_open"),
    Input(ids.input.pv.bipartite.button, "active"),
    prevent_initial_callback=True,
)
def collapse_distribution(active):
    return active
