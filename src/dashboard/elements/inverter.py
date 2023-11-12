from constants.containter import *
from constants.ids import ids
from dashboard.components import *
from data.ram_cached import ram_cache


def manufacturer_dropdown() -> dbc.Container:
    return labelled_dropdown(
        "Inverter Manufacturer",
        ids.input.pv.inverter.manufacturer.input,
        list(ram_cache.inverters.keys()),
        PVSystemData.Inverter.manufacturer,
        store_id=ids.input.pv.inverter.manufacturer.store,
    )


def series_dropdown() -> dbc.Container:
    return labelled_dropdown(
        "Inverter Series",
        ids.input.pv.inverter.series.input,
        list(ram_cache.inverters[PVSystemData.Inverter.manufacturer].keys()),
        PVSystemData.Inverter.series,
        store_id=ids.input.pv.inverter.series.store,
    )


def model_dropdown() -> dbc.Container:
    return labelled_dropdown(
        "Inverter Model",
        ids.input.pv.inverter.model.input,
        list(
            ram_cache.inverters[PVSystemData.Inverter.manufacturer][
                PVSystemData.Inverter.series
            ].keys()
        ),
        PVSystemData.Inverter.model,
        store_id=ids.input.pv.inverter.model.store,
    )


def custom_button() -> dbc.Container:
    return dbc.Container(
        dbc.Button(
            "Add Inverter",
            id=ids.input.pv.inverter.custom.button,
            active=False,
        ),
        fluid=True,
    )


def save_custom_button() -> dbc.Fade:
    return dbc.Fade(
        dbc.Button(
            "Save Inverter",
            id=ids.input.pv.inverter.custom.save,
            disabled=True,
        ),
        id=ids.input.pv.inverter.custom.fade,
        is_in=False,
    )


def saved_custom_alert() -> dbc.Alert:
    return dbc.Alert(
        "Saved Inverter",
        id=ids.input.pv.inverter.custom.success,
        dismissable=True,
        is_open=False,
        color="success",
    )


def stats() -> dbc.Accordion:
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
