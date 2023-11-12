from dash import dash_table

from constants.ids import ids
from dashboard.components import *
from dashboard.figures import *


def label() -> dbc.Label:
    return dbc.Label(
        "Simulation Results",
        style={"text-align": "left", "font-size": "3vh  "},
    )


def table() -> dash_table.DataTable:
    return dash_table.DataTable(
        id=ids.output.table,
        data=[{}],
        columns=get_table_columns(OptimizationState.Fix, OptimizationState.Fix, False),
        style_cell={
            "textAlign": "right",
            "whiteSpace": "pre-line",
            "font-family": "sans-serif",
        },
        style_cell_conditional=[{"if": {"column_id": ""}, "textAlign": "left"}],
        style_as_list_view=True,
        style_header={
            "border-top": "none",
            "font-family": "sans-serif",
            "background-color": "white",
        },
    )


def plot() -> dcc.Graph:
    return dcc.Graph(
        id=ids.output.graph,
        figure=get_graph_figure(
            PVSystemData.bipartite, PVSystemData.side1, PVSystemData.side2
        ),
        style={"width": "100%", "height": "30vh"},
    )
