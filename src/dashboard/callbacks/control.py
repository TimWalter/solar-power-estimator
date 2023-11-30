from dataclasses import asdict
from itertools import islice

import dash
from dacite import from_dict
from dash import Input, Output, State, no_update
from pvlib.location import Location
import dash_bootstrap_components as dbc


import data.disk_cached
from constants.containter import *
from constants.ids import ids
from dashboard.figures import get_table_data, get_graph_figure
from optimization import optimize
from simulation import simulate


def no_import_removal():
    pass


@dash.callback(
    output=[
        Output(ids.output.table, "data"),
        Output(ids.output.graph, "figure"),
    ],
    inputs=dict(n_clicks=Input(ids.control.start, "n_clicks")),
    state=dict(
        location=dict(
            latitude=State(ids.input.location.latitude, "value"),
            longitude=State(ids.input.location.longitude, "value"),
            altitude=State(ids.input.location.altitude, "value"),
        ),
        datetimerange=dict(
            start=State(ids.input.time, "start_date"),
            end=State(ids.input.time, "end_date"),
        ),
        pvsystemdata=dict(
            bipartite=State(ids.input.pv.bipartite.button, "active"),
            side1=State(ids.input.pv.bipartite.side1, "value"),
            side2=State(ids.input.pv.bipartite.side2, "value"),
            inverter=dict(
                manufacturer=State(ids.input.pv.inverter.manufacturer.input, "value"),
                series=State(ids.input.pv.inverter.series.input, "value"),
                model=State(ids.input.pv.inverter.model.input, "value"),
                stats={key: State(idx, "value") for key, idx in
                       islice(asdict(ids.input.pv.inverter.stats).items(), 1, None)},
            ),
        ),
        module=dict(
            panel=dict(
                manufacturer=State(ids.input.pv.panel.manufacturer.input, "value"),
                series=State(ids.input.pv.panel.series.input, "value"),
                model=State(ids.input.pv.panel.model.input, "value"),
                stats={key: State(idx, "value") for key, idx in
                       islice(asdict(ids.input.pv.panel.stats).items(), 1, None)},
            ),
            case=State(ids.input.pv.case, "value"),
            tilt=State(ids.input.pv.tilt.fix.input, "value"),
            azimuth=State(ids.input.pv.azimuth.fix.input, "value"),
        ),
        tilt_info=dict(
            value=State(ids.input.pv.tilt.fix.input, "value"),
            min=State(ids.input.pv.tilt.constrain.min, "value"),
            max=State(ids.input.pv.tilt.constrain.max, "value"),
            state=State(ids.input.pv.tilt.radio, "value"),
        ),
        azimuth_info=dict(
            value=State(ids.input.pv.azimuth.fix.input, "value"),
            min=State(ids.input.pv.azimuth.constrain.min, "value"),
            max=State(ids.input.pv.azimuth.constrain.max, "value"),
            state=State(ids.input.pv.azimuth.radio, "value"),
        ),
    ),
    background=True,
    running=[
        (Output(ids.control.start, "disabled"), True, False),
        (Output(ids.control.cancel.button, "disabled"), False, True),
        (Output(ids.control.cancel.fade, "is_in"), True, False),
    ],
    cancel=[Input(ids.control.cancel.button, "n_clicks")],
    progress=Output(ids.control.progress_bar, "children"),
    progress_default=dbc.Progress(value=0, bar=True, label="Start Simulation"),
    prevent_initial_callback=True,
)
def start_simulation(set_progress, n_clicks, location, datetimerange, pvsystemdata, module, tilt_info, azimuth_info):
    if n_clicks is None:
        return no_update, no_update

    location = Location(**location)
    time = DateTimeRange(
        datetime.strptime(datetimerange["start"], "%Y-%m-%dT%H:%M:%S"),
        datetime.strptime(datetimerange["end"], "%Y-%m-%dT%H:%M:%S"),
    )
    pv_system_data = from_dict(PVSystemData, pvsystemdata)
    module["panel"]["stats"]["cell_type"] = CellType.from_cec(module["panel"]["stats"]["cell_type"])
    module["case"] = Case[module["case"]]
    module = from_dict(PVSystemData.Module, module)
    pv_system_data.make_consistent_modules(module)

    tilt_info = OptimizableVariable(**tilt_info)
    azimuth_info = OptimizableVariable(**azimuth_info)

    set_progress([dbc.Progress(value=20, bar=True, label="Fetching Data")])
    # Step 1: Fetch Data
    radiation = data.disk_cached.fetch_radiation(location, time)
    set_progress([dbc.Progress(value=40, bar=True, label="Optimizing")])
    # Step 2: Optimization
    module.tilt, module.azimuth = optimize(location, pv_system_data, radiation, tilt_info, azimuth_info)
    pv_system_data.make_consistent_modules(module)
    set_progress([dbc.Progress(value=80, bar=True, label="Simulating")])
    # Step 3: Simulation
    result = simulate(location, pv_system_data, radiation)
    set_progress([dbc.Progress(value=100, bar=True, label="Done")])

    return (
        get_table_data(pv_system_data, result, tilt_info, azimuth_info),
        get_graph_figure(pv_system_data.bipartite, pv_system_data.side1, pv_system_data.side2, result),
    )
