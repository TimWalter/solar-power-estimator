from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

from dashboard.figures import get_empty_table, progress_figure, map_figure
from data.containter import *
from constants.ids import *


def horizontal_line():
    return html.Hr(
        style={"borderTop": "0.1vh solid #888", "width": "90%", "margin": "4vh auto"}
    )


def dropdown_input(
    title: str, idx: str, default_value: str, options: list
) -> dbc.Container:
    return dbc.Container(
        [
            dbc.Label(title),
            dcc.Dropdown(
                id=idx,
                options=options,
                value=default_value,
                searchable=True,
                clearable=False,
            ),
        ],
        fluid=True,
    )


def get_map(pos: Position) -> dcc.Graph:
    return dcc.Graph(
        id=MAP_ID,
        figure=map_figure(pos),
        config={
            "autosizable": True,
            "scrollZoom": True,
            "modeBarButtonsToRemove": ["lasso2d", "select2d"],
        },
        style={
            "padding-top": "1vh",
            "padding-bottom": "1vh",
        },
        className="transparent-modebar",
    )


def numerical_input(title: str, idx: str, initial_value: str) -> dbc.Container:
    return dbc.Container(
        [
            dbc.Label(title),
            dbc.Input(id=idx, type="number", value=initial_value),
        ],
        fluid=True,
    )


def date_range_input(title: str, idx: str, initial_value: tuple) -> dbc.Container:
    return dbc.Container(
        [
            dbc.Label(title, style={"margin-right": "2vh"}),
            dcc.DatePickerRange(
                id=idx,
                start_date=initial_value[0],
                end_date=initial_value[1],
                display_format="DD.MM.YYYY",
                min_date_allowed=datetime(2005, 1, 1),
                max_date_allowed=datetime(2020, 12, 31),
            ),
        ],
        fluid=True, className="d-flex justify-content-center"
    )


def progress_bar() -> dbc.Container:
    return dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    html.Div(id=NON_LOADING_ID),
                    width=1,
                    align=("center",),
                ),
                dbc.Col(
                    html.Img(
                        src=r"../assets/loading_icon.gif",
                        alt="image",
                        id=LOADING_ICON_ID,
                        hidden=False,
                        style={"padding": 10, "width": "100%", "max-height": "100%"},
                    ),
                    width=1,
                    align="center",
                ),
                dbc.Col(
                    dcc.Graph(
                        id=PROGRESS_BAR_ID,
                        figure=progress_figure(0),
                        config={"displayModeBar": False},
                        style={"border": "0.1vh solid #888", "height": "10vh"},
                    ),
                    width=10,
                    align="center",
                ),
            ],
        )
    )


def output_table(idx: str) -> dash_table.DataTable:
    data, columns = get_empty_table()

    return dash_table.DataTable(
        id=idx,
        data=data.to_dict("records"),
        columns=columns,
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


def output_plot(idx: str) -> dcc.Graph:
    return dcc.Graph(
        id=idx, figure=go.Figure(), style={"width": "100%", "height": "30vh"}
    )
