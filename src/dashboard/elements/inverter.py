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
                    labelled_input_group(
                        ["P", html.Sub("ac")],
                        "AC power rating of the inverter",
                        ids.input.pv.inverter.stats.paco,
                        default_inverter["Paco"],
                        "W",
                        disabled=True,
                    ),
                    labelled_input_group(
                        ["P", html.Sub("dc")],
                        "DC power required to achieve the power rating",
                        ids.input.pv.inverter.stats.pdco,
                        default_inverter["Pdco"],
                        "W",
                        disabled=True,
                    ),
                    labelled_input_group(
                        ["V", html.Sub("dc")],
                        "DC voltage required to achieve the power rating",
                        ids.input.pv.inverter.stats.vdco,
                        default_inverter["Vdco"],
                        "V",
                        disabled=True,
                    ),
                    labelled_input_group(
                        ["P", html.Sub("s")],
                        "DC power required to start the inversion process",
                        ids.input.pv.inverter.stats.pso,
                        default_inverter["Pso"],
                        "W",
                        disabled=True,
                    ),
                    labelled_input_group(
                        ["C", html.Sub("0")],
                        "AC-DC Coefficient",
                        ids.input.pv.inverter.stats.c0,
                        default_inverter["C0"],
                        "1/V",
                        disabled=True,
                    ),
                    labelled_input_group(
                        ["C", html.Sub("1")],
                        "DC Power-Voltage Coefficient at power rating",
                        ids.input.pv.inverter.stats.c1,
                        default_inverter["C1"],
                        "1/V",
                        disabled=True,
                    ),
                    labelled_input_group(
                        ["C", html.Sub("2")],
                        "DC Power-Voltage Coefficient at start of inversion",
                        ids.input.pv.inverter.stats.c2,
                        default_inverter["C2"],
                        "1/V",
                        disabled=True,
                    ),
                    labelled_input_group(
                        ["C", html.Sub("3")],
                        "C0-Voltage(DC) coefficient",
                        ids.input.pv.inverter.stats.c3,
                        default_inverter["C3"],
                        "1/V",
                        disabled=True,
                    ),
                    labelled_input_group(
                        ["P", html.Sub("nt")],
                        "AC Night Tare",
                        ids.input.pv.inverter.stats.pnt,
                        default_inverter["Pnt"],
                        "W",
                        disabled=True,
                    ),
                ],
                title="Inverter Stats",
            )
        ],
        id=ids.input.pv.inverter.stats.accordion,
        start_collapsed=True,
    )
