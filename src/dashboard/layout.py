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
            dbc.Row(dbc.Col(input_section())),
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


def input_section() -> dbc.Container:
    return dbc.Container(
        [
            dbc.Row(dbc.Col(location_subsection())),
            horizontal_line(),
            dbc.Row(dbc.Col(time()), justify="center"),
            horizontal_line(),
            dbc.Row(dbc.Col(pv_subsection())),
        ],
        fluid=True,
    )


def location_subsection() -> dbc.Container:
    return dbc.Container(
        [
            dbc.Row(dbc.Col(location.name_dropdown())),
            dbc.Row(dbc.Col(location.map_graph())),
            dbc.Row(
                [
                    dbc.Col(
                        location.latitude_input(),
                        width=3,
                    ),
                    dbc.Col(
                        location.longitude_input(),
                        width=3,
                    ),
                    dbc.Col(
                        location.altitude_input(),
                        width=3,
                    ),
                ],
                justify="center",
            ),
        ],
        fluid=True,
    )


def pv_subsection() -> dbc.Container:
    return dbc.Container(
        [
            dbc.Row(dbc.Col(panel_subsubsection())),
            dbc.Row(
                [
                    dbc.Col(case_dropdown()),
                    dbc.Col(number_of_modules_input()),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(tilt_input()),
                    dbc.Col(azimuth_input()),
                    dbc.Col(bipartite_input()),
                ],
                align="end",
            ),
            dbc.Row([
                dbc.Col(inverter.manufacturer_dropdown()),
                dbc.Col(inverter.series_dropdown()),
                dbc.Col(inverter.model_dropdown()),
                dbc.Col(inverter.custom_button()),
                dbc.Col(inverter.save_custom_button()),
                dbc.Col(inverter.saved_custom_alert())
            ], align="end"),
            dbc.Row(dbc.Col(inverter.stats())),
        ],
        fluid=True,
    )


def panel_subsubsection() -> dbc.Container:
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Col(panel.manufacturer_dropdown()),
                            dbc.Col(panel.series_dropdown()),
                            dbc.Col(panel.model_dropdown()),
                        ]
                    ),
                    dbc.Col(
                        [
                            panel.saved_custom_alert(),
                            panel.custom_button(),
                            panel.save_custom_button(),
                        ]
                    ),
                    dbc.Col(panel.stats()),
                ]
            )
        ],
        fluid=True
    )


def control_section() -> dbc.Container:
    return dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(control.start_button(), width={"size": 5, "offset": 2}),
                                dbc.Col(control.cancel_button(), width=5),
                            ]
                        ),
                    ],
                    width=2,
                    align="center",
                ),
                dbc.Col(control.progress_bar(), width=10),
            ]
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
