from dash import dash_table

from constants.ids import ids
from dashboard.components import *
from dashboard.figures import *
from constants.containter import *
from data.ram_cached import ram_cache


def title() -> html.H1:
    return html.H1("Solar Power Estimation", style={"text-align": "center"})


def location_dropdown() -> dbc.Container:
    return labelled_dropdown(
        "Location", ids.input.location.name, [Location().name], Location().name
    )


def map_graph() -> dcc.Graph:
    return dcc.Graph(
        id=ids.input.location.map,
        figure=map_figure(Location().latitude, Location().longitude),
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
    return labelled_input("Latitude", ids.input.location.latitude, Location().latitude)


def longitude_input() -> dbc.Container:
    return labelled_input(
        "Longitude", ids.input.location.longitude, Location().longitude
    )


def altitude_input() -> dbc.Container:
    return labelled_input("Altitude", ids.input.location.altitude, Location().altitude)


def simulation_time_daterangepicker() -> dbc.Container:
    return dbc.Container(
        [
            dbc.Label("Simulation time", style={"margin-right": "2vh"}),
            dcc.DatePickerRange(
                id=ids.input.time,
                start_date=DateTimeRange.start,
                end_date=DateTimeRange.end,
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
        list(ram_cache.panels.keys()),
        PVSystemData.Module.Panel.manufacturer,
        store_id=ids.input.pv.panel.custom.manufacturer_store,
    )


def panel_series_dropdown() -> dbc.Container:
    return labelled_dropdown(
        "Panel Series",
        ids.input.pv.panel.series,
        list(ram_cache.panels[PVSystemData.Module.Panel.manufacturer].keys()),
        PVSystemData.Module.Panel.series,
        store_id=ids.input.pv.panel.custom.series_store,
    )


def panel_model_dropdown() -> dbc.Container:
    return labelled_dropdown(
        "Panel Model",
        ids.input.pv.panel.model,
        list(
            ram_cache.panels[PVSystemData.Module.Panel.manufacturer][
                PVSystemData.Module.Panel.series
            ].keys()
        ),
        PVSystemData.Module.Panel.model,
        store_id=ids.input.pv.panel.custom.model_store,
    )


def custom_panel_button() -> dbc.Container:
    return dbc.Container(
        dbc.Button(
            "Add Panel",
            id=ids.input.pv.panel.custom.button,
            active=False,
        ),
        fluid=True,
    )


def save_custom_panel_button() -> dbc.Fade:
    return dbc.Fade(
        dbc.Button(
            "Save Panel",
            id=ids.input.pv.panel.custom.save,
            disabled=True,
        ),
        id=ids.input.pv.panel.custom.fade,
        is_in=False,
    )


def saved_custom_panel_alert() -> dbc.Alert:
    return dbc.Alert(
        "Saved Panel",
        id=ids.input.pv.panel.custom.success,
        dismissable=True,
        is_open=False,
        color="success",
    )


def panel_stats() -> dbc.Accordion:
    default_panel = ram_cache.panels[PVSystemData.Module.Panel.manufacturer][
        PVSystemData.Module.Panel.series
    ][PVSystemData.Module.Panel.model]
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                labelled_input_group(
                                    ["V", html.Sub("mp")],
                                    "Maximum power point voltage",
                                    "V",
                                    ids.input.pv.panel.stats.v_mp,
                                    default_panel["V_mp_ref"],
                                    disabled=True,
                                ),
                            ),
                            dbc.Col(
                                labelled_input_group(
                                    ["I", html.Sub("mp")],
                                    "Maximum power point current",
                                    "A",
                                    ids.input.pv.panel.stats.i_mp,
                                    default_panel["I_mp_ref"],
                                    disabled=True,
                                ),
                            ),
                            dbc.Col(
                                labelled_input_group(
                                    ["V", html.Sub("oc")],
                                    "Open circuit voltage",
                                    "V",
                                    ids.input.pv.panel.stats.v_oc,
                                    default_panel["V_oc_ref"],
                                    disabled=True,
                                ),
                            ),
                            dbc.Col(
                                labelled_input_group(
                                    ["I", html.Sub("sc")],
                                    "Short circuit current",
                                    "A",
                                    ids.input.pv.panel.stats.i_sc,
                                    default_panel["I_sc_ref"],
                                    disabled=True,
                                ),
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                labelled_input_group(
                                    ["T", html.Sub(["V", html.Sub("oc")])],
                                    "Temperature coefficient of open circuit voltage",
                                    "V/°C",
                                    ids.input.pv.panel.stats.t_v_oc,
                                    default_panel["beta_oc"],
                                    disabled=True,
                                ),
                            ),
                            dbc.Col(
                                labelled_input_group(
                                    ["T", html.Sub(["I", html.Sub("sc")])],
                                    "Temperature coefficient of short circuit current",
                                    "A/°C",
                                    ids.input.pv.panel.stats.t_i_sc,
                                    default_panel["alpha_sc"],
                                    disabled=True,
                                ),
                            ),
                            dbc.Col(
                                labelled_input_group(
                                    ["T", html.Sub(["P", html.Sub("mp")])],
                                    "Temperature coefficient of maximum power point voltage",
                                    "V/°C",
                                    ids.input.pv.panel.stats.t_p_mp,
                                    default_panel["gamma_r"],
                                    disabled=True,
                                ),
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                labelled_dropdown(
                                    "Technology",
                                    ids.input.pv.panel.stats.technology,
                                    [
                                        "Mono-c-Si",
                                        "Multi-c-Si",
                                        "Poly-c-Si",
                                        "CIS",
                                        "CIGS",
                                        "CdTe",
                                        "Amorphous",
                                    ],
                                    default_panel["Technology"],
                                    disabled=True,
                                ),
                            ),
                            dbc.Col(
                                labelled_input_group(
                                    ["N", html.Sub("s")],
                                    "Number of cells in series",
                                    "",
                                    ids.input.pv.panel.stats.n_cells_series,
                                    default_panel["N_s"],
                                    disabled=True,
                                ),
                            ),
                        ]
                    ),
                ],
                title="Panel Stats",
            )
        ],
        id=ids.input.pv.panel.stats.accordion,
        flush=True,
        start_collapsed=True,
    )


def case_dropdown() -> dbc.Container:
    return labelled_dropdown(
        "Case",
        ids.input.pv.case,
        [case.name for case in Cases],
        PVSystemData.Module.case.name,
    )


def number_of_modules_input() -> dbc.Container:
    return labelled_input(
        "Number of modules",
        ids.input.pv.number_of_modules,
        len(PVSystemData.modules),
    )


def tilt_input() -> dbc.Container:
    return labelled_optimizable_number_input(
        "Tilt",
        ids.input.pv.tilt.radio,
        OptimizationState.Fix,
        ids.input.pv.tilt.fix.collapse,
        ids.input.pv.tilt.fix.input,
        PVSystemData.Module.tilt,
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
        OptimizationState.Fix,
        ids.input.pv.azimuth.fix.collapse,
        ids.input.pv.azimuth.fix.input,
        PVSystemData.Module.azimuth,
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
                        active=PVSystemData.bipartite,
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
                                        value=PVSystemData.side1,
                                    ),
                                    width=6,
                                ),
                                dbc.Col(
                                    dbc.Input(
                                        id=ids.input.pv.bipartite.side2,
                                        type="number",
                                        value=PVSystemData.side2,
                                        disabled=True,
                                    ),
                                    width=6,
                                ),
                            ]
                        ),
                        id=ids.input.pv.bipartite.collapse,
                        is_open=False,
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
        list(ram_cache.inverters.keys()),
        PVSystemData.Inverter.manufacturer,
        store_id=ids.input.pv.inverter.custom.manufacturer_store,
    )


def inverter_series_dropdown() -> dbc.Container:
    return labelled_dropdown(
        "Inverter Series",
        ids.input.pv.inverter.series,
        list(ram_cache.inverters[PVSystemData.Inverter.manufacturer].keys()),
        PVSystemData.Inverter.series,
        store_id=ids.input.pv.inverter.custom.series_store,
    )


def inverter_model_dropdown() -> dbc.Container:
    return labelled_dropdown(
        "Inverter Model",
        ids.input.pv.inverter.model,
        list(
            ram_cache.inverters[PVSystemData.Inverter.manufacturer][
                PVSystemData.Inverter.series
            ].keys()
        ),
        PVSystemData.Inverter.model,
        store_id=ids.input.pv.inverter.custom.model_store,
    )


def custom_inverter_button() -> dbc.Container:
    return dbc.Container(
        dbc.Button(
            "Add Inverter",
            id=ids.input.pv.inverter.custom.button,
            active=False,
        ),
        fluid=True,
    )


def save_custom_inverter_button() -> dbc.Fade:
    return dbc.Fade(
        dbc.Button(
            "Save Inverter",
            id=ids.input.pv.inverter.custom.save,
            disabled=True,
        ),
        id=ids.input.pv.inverter.custom.fade,
        is_in=False,
    )


def saved_custom_inverter_alert() -> dbc.Alert:
    return dbc.Alert(
        "Saved Inverter",
        id=ids.input.pv.inverter.custom.success,
        dismissable=True,
        is_open=False,
        color="success",
    )


def inverter_stats() -> dbc.Accordion:
    default_inverter = ram_cache.inverters[PVSystemData.Inverter.manufacturer][
        PVSystemData.Inverter.series
    ][PVSystemData.Inverter.model]
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                labelled_input_group(
                                    ["P", html.Sub("ac_o")],
                                    "AC power rating of the inverter",
                                    "W",
                                    ids.input.pv.inverter.stats.paco,
                                    default_inverter["Paco"],
                                    disabled=True,
                                ),
                            ),
                            dbc.Col(
                                labelled_input_group(
                                    ["P", html.Sub("dc_o")],
                                    "DC power input that results in Paco output at reference voltage Vdco",
                                    "W",
                                    ids.input.pv.inverter.stats.pdco,
                                    default_inverter["Pdco"],
                                    disabled=True,
                                ),
                            ),
                            dbc.Col(
                                labelled_input_group(
                                    ["V", html.Sub("dc_o")],
                                    "DC voltage at which the AC power rating is achieved with Pdco power input",
                                    "V",
                                    ids.input.pv.inverter.stats.vdco,
                                    default_inverter["Vdco"],
                                    disabled=True,
                                ),
                            ),
                            dbc.Col(
                                labelled_input_group(
                                    ["P", html.Sub("s_o")],
                                    "DC power required to start the inversion process, or self-consumption by inverter",
                                    "W",
                                    ids.input.pv.inverter.stats.pso,
                                    default_inverter["Pso"],
                                    disabled=True,
                                ),
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                labelled_input_group(
                                    ["C", html.Sub("0")],
                                    "Parameter defining the curvature (parabolic) of the relationship between AC power and DC power at the reference operating condition",
                                    "1/V",
                                    ids.input.pv.inverter.stats.c0,
                                    default_inverter["C0"],
                                    disabled=True,
                                ),
                            ),
                            dbc.Col(
                                labelled_input_group(
                                    ["C", html.Sub("1")],
                                    "Empirical coefficient allowing Pdco to vary linearly with DC voltage input",
                                    "1/V",
                                    ids.input.pv.inverter.stats.c1,
                                    default_inverter["C1"],
                                    disabled=True,
                                ),
                            ),
                            dbc.Col(
                                labelled_input_group(
                                    ["C", html.Sub("2")],
                                    "Empirical coefficient allowing Pso to vary linearly with DC voltage input",
                                    "1/V",
                                    ids.input.pv.inverter.stats.c2,
                                    default_inverter["C2"],
                                    disabled=True,
                                ),
                            ),
                            dbc.Col(
                                labelled_input_group(
                                    ["C", html.Sub("3")],
                                    "Empirical coefficient allowing C0 to vary linearly with DC voltage input",
                                    "1/V",
                                    ids.input.pv.inverter.stats.c3,
                                    default_inverter["C3"],
                                    disabled=True,
                                ),
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Col(
                                    labelled_input_group(
                                        ["P", html.Sub("nt")],
                                        "AC power consumed by the inverter at night (night tare)",
                                        "W",
                                        ids.input.pv.inverter.stats.pnt,
                                        default_inverter["Pnt"],
                                        disabled=True,
                                    ),
                                ),
                            ),
                        ]
                    ),
                ],
                title="Inverter Stats",
            )
        ],
        id=ids.input.pv.inverter.stats.accordion,
        flush=True,
        start_collapsed=True,
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


def output_plot() -> dcc.Graph:
    return dcc.Graph(
        id=ids.output.graph,
        figure=get_graph_figure(
            PVSystemData.bipartite, PVSystemData.side1, PVSystemData.side2
        ),
        style={"width": "100%", "height": "30vh"},
    )
