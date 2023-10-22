from constants.custom_components import *
from dashboard.elements import *


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
            dbc.Row(dbc.Col(simulation_time_daterangepicker()), justify="center"),
            horizontal_line(),
            dbc.Row(dbc.Col(pv_subsection())),
        ],
        fluid=True,
    )


def location_subsection() -> dbc.Container:
    return dbc.Container(
        [
            dbc.Row(dbc.Col(location_dropdown())),
            dbc.Row(dbc.Col(map_graph())),
            dbc.Row(
                [
                    dbc.Col(
                        latitude_input(),
                        width=3,
                    ),
                    dbc.Col(
                        longitude_input(),
                        width=3,
                    ),
                    dbc.Col(
                        altitude_input(),
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
            dbc.Row(
                [
                    dbc.Col(panel_manufacturer_dropdown()),
                    dbc.Col(panel_series_dropdown()),
                    dbc.Col(panel_model_dropdown()),
                ]
            ),
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
                dbc.Col(inverter_manufacturer_dropdown()),
                dbc.Col(inverter_series_dropdown()),
                dbc.Col(inverter_model_dropdown()),
            ]),
        ],
        fluid=True,
    )


def control_section() -> dbc.Container:
    return dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(start_button(), width={"size": 5, "offset": 2}),
                                dbc.Col(cancel_button(), width=5),
                            ]
                        ),
                    ],
                    width=2,
                    align="center",
                ),
                dbc.Col(progress_bar(), width=10),
            ]
        ),
        fluid=True,
    )


def output_section() -> dbc.Container:
    return dbc.Container(
        [
            result_label(),
            dbc.Stack(
                [
                    output_table(),
                    output_plot(),
                ]
            ),
        ],
        fluid=True,
    )
