import dash
from dash import Input, Output, State

from constants.containter import *
from constants.ids import ids
from dashboard.figures import get_table_columns, get_graph_figure


def no_import_removal():
    pass


@dash.callback(
    Output(ids.output.table, "columns"),
    Output(ids.output.graph, "figure", allow_duplicate=True),
    Input(ids.input.pv.tilt.radio, "value"),
    Input(ids.input.pv.azimuth.radio, "value"),
    Input(ids.input.pv.bipartite.button, "active"),
    State(ids.input.pv.bipartite.side1, "value"),
    State(ids.input.pv.bipartite.side2, "value"),
    prevent_initial_call="initial_duplicate",
)
def mock_outputs(tilt_optimization_state, azimuth_optimization_state, bipartite, side1, side2):
    return get_table_columns(
        OptimizationState(tilt_optimization_state),
        OptimizationState(azimuth_optimization_state),
        bipartite,
    ), get_graph_figure(bipartite, side1, side2)
