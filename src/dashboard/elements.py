from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS


from dashboard.figures import (
    map_figure,
    progress_figure,
    get_table_columns,
    get_graph_figure,
)
from constants.ids import ids
from constants.defaults import *
from constants.custom_components import *
from data.containter import *
from data import ram_cached


def title() -> html.H1:
    return html.H1("Solar Power Estimation", style={"text-align": "center"})


def location_dropdown() -> dbc.Container:
    return labelled_dropdown("Location", ids.input.location.name, [LOCATION], LOCATION)


def map_graph() -> dcc.Graph:
    return dcc.Graph(
        id=ids.input.location.map,
        figure=map_figure(LATITUDE, LONGITUDE),
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


def latitude_input() -> dbc.Container:
    return labelled_number_input("Latitude", ids.input.location.latitude, LATITUDE)


def longitude_input() -> dbc.Container:
    return labelled_number_input("Longitude", ids.input.location.longitude, LONGITUDE)


def altitude_input() -> dbc.Container:
    return labelled_number_input("Altitude", ids.input.location.altitude, ALTITUDE)


def simulation_time_daterangepicker() -> dbc.Container:
    return dbc.Container(
        [
            dbc.Label("Simulation time", style={"margin-right": "2vh"}),
            dcc.DatePickerRange(
                id=ids.input.time,
                start_date=TIME[0],
                end_date=TIME[1],
                display_format="DD.MM.YYYY",
                min_date_allowed=datetime(2005, 1, 1),
                max_date_allowed=datetime(2020, 12, 31),
            ),
        ],
        fluid=True,
        className="d-flex justify-content-center",
    )


def panel_manufacturer_dropdown() -> dbc.Container:
    return labelled_dropdown(
        "Panel Manufacturer",
        ids.input.pv.panel.manufacturer,
        list(ram_cached.fetch_modules().keys()),
        PANEL_MANUFACTURER,
    )


def panel_series_dropdown() -> dbc.Container:
    return labelled_dropdown(
        "Panel Series",
        ids.input.pv.panel.series,
        list(ram_cached.fetch_modules()[PANEL_MANUFACTURER].keys()),
        PANEL_SERIES,
    )


def panel_model_dropdown() -> dbc.Container:
    return labelled_dropdown(
        "Panel Model",
        ids.input.pv.panel.model,
        list(ram_cached.fetch_modules()[PANEL_MANUFACTURER][PANEL_SERIES].keys()),
        PANEL_MODEL,
    )


def panel_stats() -> dbc.Accordion:
    default_panel = ram_cached.fetch_modules()[PANEL_MANUFACTURER][PANEL_SERIES][
        PANEL_MODEL
    ]
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                labelled_input_group(
                                    [
                                        "Maximum power point voltage (V",
                                        html.Sub("mp"),
                                        ") [V]",
                                    ],
                                    ids.input.pv.panel.stats.v_mp,
                                    default_panel["V_mp_ref"],
                                ),
                            ),
                            dbc.Col(
                                labelled_input_group(
                                    [
                                        "Maximum power point current (I",
                                        html.Sub("mp"),
                                        ") [A]",
                                    ],
                                    ids.input.pv.panel.stats.i_mp,
                                    default_panel["I_mp_ref"],
                                ),
                            ),
                            dbc.Col(
                                labelled_input_group(
                                    [
                                        "Open circuit voltage (V",
                                        html.Sub("oc"),
                                        ") [V]",
                                    ],
                                    ids.input.pv.panel.stats.v_oc,
                                    default_panel["V_oc_ref"],
                                ),
                            ),
                            dbc.Col(
                                labelled_input_group(
                                    [
                                        "Short circuit current (I",
                                        html.Sub("sc"),
                                        ") [A]",
                                    ],
                                    ids.input.pv.panel.stats.i_sc,
                                    default_panel["I_sc_ref"],
                                ),
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                labelled_input_group(
                                    [
                                        "Temperature coefficient of open circuit voltage (T",
                                        html.Sub(["V", html.Sub("oc")]),
                                        ") [V/°C]",
                                    ],
                                    ids.input.pv.panel.stats.t_v_oc,
                                    default_panel["beta_oc"],
                                ),
                            ),
                            dbc.Col(
                                labelled_input_group(
                                    [
                                        "Temperature coefficient of short circuit current (T",
                                        html.Sub(["V", html.Sub("sc")]),
                                        ") [A/°C]",
                                    ],
                                    ids.input.pv.panel.stats.t_i_sc,
                                    default_panel["alpha_sc"],
                                ),
                            ),
                            dbc.Col(
                                labelled_input_group(
                                    [
                                        "Temperature coefficient of maximum power point voltage (T",
                                        html.Sub(["V", html.Sub("mp")]),
                                        ") [V/°C]",
                                    ],
                                    ids.input.pv.panel.stats.t_p_mp,
                                    default_panel["gamma_r"],
                                ),
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                labelled_input_group(
                                    ["Technology"],
                                    ids.input.pv.panel.stats.technology,
                                    default_panel["Technology"],
                                    "text"
                                ),
                            ),
                            dbc.Col(
                                labelled_input_group(
                                    ["Number of cells in series"],
                                    ids.input.pv.panel.stats.n_cells_series,
                                    default_panel["N_s"],
                                ),
                            ),
                        ]
                    ),
                ],
                title="Panel Stats",
                id=ids.input.pv.panel.stats.accordion,
            )
        ],
        flush=True,
        start_collapsed=True,
    )


def case_dropdown() -> dbc.Container:
    return labelled_dropdown(
        "Case",
        ids.input.pv.case,
        list(TEMPERATURE_MODEL_PARAMETERS["sapm"].keys()),
        CASE,
    )


def number_of_modules_input() -> dbc.Container:
    return labelled_number_input(
        "Number of modules", ids.input.pv.number_of_modules, NUMBER_OF_MODULES
    )


def tilt_input() -> dbc.Container:
    return labelled_optimizable_number_input(
        "Tilt",
        ids.input.pv.tilt.radio,
        OPT_TILT,
        ids.input.pv.tilt.fix.collapse,
        ids.input.pv.tilt.fix.input,
        TILT,
        ids.input.pv.tilt.constrain.collapse,
        ids.input.pv.tilt.constrain.min,
        0,
        ids.input.pv.tilt.constrain.max,
        90,
    )


def azimuth_input() -> dbc.Container:
    return labelled_optimizable_number_input(
        "Azimuth",
        ids.input.pv.azimuth.radio,
        OPT_AZIMUTH,
        ids.input.pv.azimuth.fix.collapse,
        ids.input.pv.azimuth.fix.input,
        AZIMUTH,
        ids.input.pv.azimuth.constrain.collapse,
        ids.input.pv.azimuth.constrain.min,
        0,
        ids.input.pv.azimuth.constrain.max,
        360,
    )


def bipartite_input() -> dbc.Container:
    return dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        "Bipartite",
                        id=ids.input.pv.bipartite.button,
                        active=BIPARTITE,
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Collapse(
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Input(
                                        id=ids.input.pv.bipartite.side1,
                                        type="number",
                                        value=NUMBER_OF_MODULES,
                                    ),
                                    width=6,
                                ),
                                dbc.Col(
                                    dbc.Input(
                                        id=ids.input.pv.bipartite.side2,
                                        type="number",
                                        value=0,
                                        disabled=True,
                                    ),
                                    width=6,
                                ),
                            ]
                        ),
                        id=ids.input.pv.bipartite.collapse,
                        is_open=BIPARTITE,
                    ),
                    width=8,
                ),
            ]
        ),
        fluid=True,
    )


def inverter_manufacturer_dropdown() -> dbc.Container:
    return labelled_dropdown(
        "Inverter Manufacturer",
        ids.input.pv.inverter.manufacturer,
        list(ram_cached.fetch_inverters().keys()),
        INVERTER_MANUFACTURER,
    )


def inverter_series_dropdown() -> dbc.Container:
    return labelled_dropdown(
        "Inverter Series",
        ids.input.pv.inverter.series,
        list(ram_cached.fetch_inverters()[INVERTER_MANUFACTURER].keys()),
        INVERTER_SERIES,
    )


def inverter_model_dropdown() -> dbc.Container:
    return labelled_dropdown(
        "Inverter Model",
        ids.input.pv.inverter.model,
        list(
            ram_cached.fetch_inverters()[INVERTER_MANUFACTURER][INVERTER_SERIES].keys()
        ),
        INVERTER_MODEL,
    )


def start_button() -> dbc.Container:
    return dbc.Container(
        dbc.Button(
            "Start Simulation",
            id=ids.control.start,
            disabled=False,
        ),
        fluid=True,
    )


def cancel_button() -> dbc.Container:
    return dbc.Container(
        dbc.Fade(
            dbc.Button(
                "Cancel Simulation",
                id=ids.control.cancel.button,
                disabled=True,
            ),
            id=ids.control.cancel.fade,
            is_in=False,
        ),
        fluid=True,
    )


def progress_bar() -> dbc.Container:
    return dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    html.Div(id=ids.control.loading.placeholder),
                    width=1,
                    align=("center",),
                ),
                dbc.Col(
                    html.Img(
                        src=r"../assets/loading_icon.gif",
                        alt="image",
                        id=ids.control.loading.gif,
                        hidden=False,
                        style={"padding": 10, "width": "100%", "max-height": "100%"},
                    ),
                    width=1,
                    align="center",
                ),
                dbc.Col(
                    dcc.Graph(
                        id=ids.control.progress_bar,
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


def result_label() -> dbc.Label:
    return dbc.Label(
        "Simulation Results",
        style={"text-align": "left", "font-size": "3vh  "},
    )


def output_table() -> dash_table.DataTable:
    return dash_table.DataTable(
        id=ids.output.table,
        data=[{}],
        columns=get_table_columns(PV()),
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


def output_plot() -> dcc.Graph:
    return dcc.Graph(
        id=ids.output.graph,
        figure=get_graph_figure(PV()),
        style={"width": "100%", "height": "30vh"},
    )
