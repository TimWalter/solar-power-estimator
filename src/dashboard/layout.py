from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS

from dashboard.elements import *
from constants.defaults import *
from constants.ids import *

from data import ram_cached


def title() -> html.H1:
    return html.H1("Solar Power Estimation", style={"text-align": "center"})


def location_subsection() -> dbc.Container:
    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    dropdown_input(
                        "Location",
                        LOCATION_NAME_ID,
                        LOCATION_NAME,
                        [LOCATION_NAME],
                    )
                ),
            ),
            dbc.Row(dbc.Col(get_map(Position(LATITUDE, LONGITUDE, ALTITUDE)))),
            dbc.Row(
                [
                    dbc.Col(
                        numerical_input("Latitude", LATITUDE_ID, LATITUDE),
                        width=3,
                    ),
                    dbc.Col(
                        numerical_input("Longitude", LONGITUDE_ID, LONGITUDE),
                        width=3,
                    ),
                    dbc.Col(
                        numerical_input("Altitude", ALTITUDE_ID, ALTITUDE),
                        width=3,
                    ),
                ],
                justify="center",
            ),
        ],
        fluid=True,
    )


def house_subsection() -> dbc.Container:
    return dbc.Container(
        [
            numerical_input("Height (Roof)", ROOF_HEIGHT_ID, ROOF_HEIGHT),
            numerical_input("Azimuth (Roof)", ROOF_AZIMUTH_ID, ROOF_AZIMUTH),
            numerical_input("Tilt (Roof)", ROOF_TILT_ID, ROOF_TILT),
        ],
        fluid=True,
    )


def pv_subsection() -> dbc.Container:
    return dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    [
                        numerical_input(
                            "Number of Panels",
                            NUMBER_OF_MODULES_ID,
                            NUMBER_OF_MODULES,
                        ),
                        numerical_input(
                            "Azimuth (Panel)", PANEL_AZIMUTH_ID, PANEL_AZIMUTH
                        ),
                        numerical_input("Tilt (Panel)", PANEL_TILT_ID, PANEL_ELEVATION),
                    ]
                ),
                dbc.Col(
                    [
                        dropdown_input(
                            "Panel Type",
                            MODULE_ID,
                            MODULE,
                            [MODULE],
                        ),
                        dropdown_input(
                            "Case",
                            CASE_ID,
                            CASE,
                            list(TEMPERATURE_MODEL_PARAMETERS["sapm"].keys()),
                        ),
                        dropdown_input(
                            "Inverter",
                            INVERTER_ID,
                            INVERTER,
                            list(ram_cached.fetch_inverters().keys()),
                        ),
                    ]
                ),
            ]
        ),
        fluid=True,
    )


def time_subsection() -> dbc.Container:
    return date_range_input("Simulation time", TIME_ID, TIME)


def input_section() -> dbc.Container:
    return dbc.Container(
        [
            dbc.Row(dbc.Col(location_subsection())),
            horizontal_line(),
            dbc.Row(
                [
                    dbc.Col(
                        house_subsection(), width=4, className="column_vertical_right"
                    ),
                    dbc.Col(pv_subsection(), width=8),
                ]
            ),
            horizontal_line(),
            dbc.Row(dbc.Col(time_subsection()), justify="center"),
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
                                dbc.Col(
                                    dbc.Button(
                                        "Start Simulation",
                                        id=START_BUTTON_ID,
                                        disabled=False,
                                    ),
                                    width={"size": 5, "offset": 2},
                                ),
                                dbc.Col(
                                    dbc.Fade(
                                        dbc.Button(
                                            "Cancel Simulation",
                                            id=CANCEL_BUTTON_ID,
                                            disabled=True,
                                        ),
                                        id=FADE_CANCEL_BUTTON_ID,
                                        is_in=False,
                                    ),
                                    width=5
                                ),
                            ]
                        ),
                    ],
                    width=2, align="center",
                ),
                dbc.Col(
                    progress_bar(),
                    width=10,
                ),
            ]
        ),
        fluid=True,
    )


def output_section() -> dbc.Container:
    return dbc.Container(
        [
            dbc.Label(
                "Simulation Results",
                style={"text-align": "left", "font-size": "3vh  "},
            ),
            dbc.Stack(
                [
                    output_table(OUTPUT_TABLE_ID),
                    output_plot(OUTPUT_GRAPH_1_ID),
                    output_plot(OUTPUT_GRAPH_2_ID),
                    output_plot(OUTPUT_GRAPH_3_ID),
                ]
            ),
        ],
        fluid=True,
    )


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
