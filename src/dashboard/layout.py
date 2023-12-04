import dashboard.elements.control as control
import dashboard.elements.inverter as inverter
import dashboard.elements.location as location
import dashboard.elements.output as output
import dashboard.elements.panel as panel
from dashboard.elements.pv import *
from dashboard.elements.time import *
from dashboard.elements.title import *


def get_layout() -> dbc.Container:
    return dbc.Container(
        [
            dbc.Row(dbc.Col(title()), justify="center"),
            dbc.Row(dbc.Col(location_subsection())),
            dbc.Row(dbc.Col(horizontal_line())),
            dbc.Row(dbc.Col(pv_subsection())),
            dbc.Row(dbc.Col(horizontal_line())),
            dbc.Row(dbc.Col(control_section())),
            dbc.Row(dbc.Col(horizontal_line())),
            dbc.Row(dbc.Col(output_section())),
        ],
        style={
            "padding": "5vh",
        },
        fluid=True,
    )


def location_subsection() -> dbc.Row:
    return dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Stack(
                        [
                            location.name_dropdown(),
                            location.latitude_input(),
                            location.longitude_input(),
                            location.altitude_input(),
                            horizontal_line(),
                            time(),
                        ],
                        gap=2,
                    )
                ],
                align="start",
                width=3,
            ),
            dbc.Col(location.map_graph(), width=9),
        ],
        justify="center",
    )


def pv_subsection() -> dbc.Container:
    return dbc.Container(
        dbc.Tabs(
            [
                dbc.Tab(
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Stack(
                                    [
                                        panel.manufacturer_dropdown(),
                                        panel.series_dropdown(),
                                        panel.model_dropdown(),
                                        dbc.Row(
                                            [
                                                dbc.Col(panel.custom_button()),
                                                dbc.Col(panel.save_custom_button()),
                                                dbc.Col(panel.saved_custom_alert()),
                                            ]
                                        ),
                                        case_dropdown(),
                                    ],
                                    gap=3,
                                ),
                                width=6,
                            ),
                            dbc.Col(
                                panel.stats(), width=6, style={"margin-top": "3vh"}
                            ),
                        ],
                        style={"margin-top": "3vh"},
                    ),
                    label="Panel",
                ),
                dbc.Tab(
                    dbc.Row(
                        dbc.Col(
                            dbc.Stack(
                                [
                                    number_of_modules_input(),
                                    tilt_input(),
                                    azimuth_input(),
                                    bipartite_input(),
                                ],
                                gap=3,
                            ),
                            width=6,
                        ),
                        style={"margin-top": "3vh"},
                    ),
                    label="Installation",
                ),
                dbc.Tab(
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Stack(
                                    [
                                        inverter.manufacturer_dropdown(),
                                        inverter.series_dropdown(),
                                        inverter.model_dropdown(),
                                        dbc.Row(
                                            [
                                                dbc.Col(inverter.custom_button()),
                                                dbc.Col(inverter.save_custom_button()),
                                                dbc.Col(inverter.saved_custom_alert()),
                                            ]
                                        ),
                                    ],
                                    gap=3,
                                ),
                                width=6,
                            ),
                            dbc.Col(
                                inverter.stats(), width=6, style={"margin-top": "3vh"}
                            ),
                        ],
                        style={"margin-top": "3vh"},
                    ),
                    label="Inverter",
                ),
            ]
        ),
        fluid=True,
    )


def control_section() -> dbc.Container:
    return dbc.Container(
        dbc.Row(
            [
                dbc.Col(control.start_button(), width=2),
                dbc.Col(control.cancel_button(), width=2),
                dbc.Col(control.progress_bar(), width=6),
            ],
            justify="center",
        ),
        fluid=True,
    )


def output_section() -> dbc.Container:
    return dbc.Container(
        [
            output.label(),
            dbc.Stack(
                [
                    output.table(),
                    output.plot(),
                ]
            ),
        ],
        fluid=True,
    )
