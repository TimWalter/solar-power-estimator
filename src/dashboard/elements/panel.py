from constants.containter import *
from constants.ids import ids
from dashboard.components import *
from data.ram_cached import ram_cache


def manufacturer_dropdown() -> dbc.Container:
    return labelled_dropdown(
        "Panel Manufacturer",
        ids.input.pv.panel.manufacturer.input,
        list(ram_cache.panels.keys()),
        PVSystemData.Module.Panel.manufacturer,
        store_id=ids.input.pv.panel.manufacturer.store,
    )


def series_dropdown() -> dbc.Container:
    return labelled_dropdown(
        "Panel Series",
        ids.input.pv.panel.series.input,
        list(ram_cache.panels[PVSystemData.Module.Panel.manufacturer].keys()),
        PVSystemData.Module.Panel.series,
        store_id=ids.input.pv.panel.series.store,
    )


def model_dropdown() -> dbc.Container:
    return labelled_dropdown(
        "Panel Model",
        ids.input.pv.panel.model.input,
        list(
            ram_cache.panels[PVSystemData.Module.Panel.manufacturer][
                PVSystemData.Module.Panel.series
            ].keys()
        ),
        PVSystemData.Module.Panel.model,
        store_id=ids.input.pv.panel.model.store,
    )


def custom_button() -> dbc.Container:
    return dbc.Container(
        dbc.Button(
            "Edit Panel",
            id=ids.input.pv.panel.custom.button,
            active=False,
        ),
        fluid=True,
    )


def save_custom_button() -> dbc.Fade:
    return dbc.Fade(
        dbc.Button(
            "Save Panel",
            id=ids.input.pv.panel.custom.save,
            disabled=True,
        ),
        id=ids.input.pv.panel.custom.fade,
        is_in=False,
    )


def saved_custom_alert() -> dbc.Alert:
    return dbc.Alert(
        "Saved Panel",
        id=ids.input.pv.panel.custom.success,
        dismissable=True,
        is_open=False,
        color="success",
    )


def stats() -> dbc.Accordion:
    default_panel = ram_cache.panels[PVSystemData.Module.Panel.manufacturer][
        PVSystemData.Module.Panel.series
    ][PVSystemData.Module.Panel.model]
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    labelled_select_group(
                        "Cell Type",
                        ids.input.pv.panel.stats.cell_type,
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
                    labelled_input_group(
                        ["N", html.Sub("s")],
                        "Number of cells in series",
                        ids.input.pv.panel.stats.n_cells_series,
                        default_panel["N_s"],
                        disabled=True,
                    ),
                    labelled_input_group(
                        ["V", html.Sub("mp")],
                        "Maximum power point voltage",
                        ids.input.pv.panel.stats.v_mp,
                        default_panel["V_mp_ref"],
                        "V",
                        disabled=True,
                    ),
                    labelled_input_group(
                        ["I", html.Sub("mp")],
                        "Maximum power point current",
                        ids.input.pv.panel.stats.i_mp,
                        default_panel["I_mp_ref"],
                        "A",
                        disabled=True,
                    ),
                    labelled_input_group(
                        ["V", html.Sub("oc")],
                        "Open circuit voltage",
                        ids.input.pv.panel.stats.v_oc,
                        default_panel["V_oc_ref"],
                        "V",
                        disabled=True,
                    ),
                    labelled_input_group(
                        ["I", html.Sub("sc")],
                        "Short circuit current",
                        ids.input.pv.panel.stats.i_sc,
                        default_panel["I_sc_ref"],
                        "A",
                        disabled=True,
                    ),
                    labelled_input_group(
                        ["T", html.Sub(["V", html.Sub("oc")])],
                        "Temperature coefficient of open circuit voltage",
                        ids.input.pv.panel.stats.t_v_oc,
                        default_panel["beta_oc"],
                        "V/°C",
                        disabled=True,
                    ),
                    labelled_input_group(
                        ["T", html.Sub(["I", html.Sub("sc")])],
                        "Temperature coefficient of short circuit current",
                        ids.input.pv.panel.stats.t_i_sc,
                        default_panel["alpha_sc"],
                        "A/°C",
                        disabled=True,
                    ),
                    labelled_input_group(
                        ["T", html.Sub(["P", html.Sub("mp")])],
                        "Temperature coefficient of maximum power point voltage",
                        ids.input.pv.panel.stats.t_p_mp,
                        default_panel["gamma_r"],
                        "V/°C",
                        disabled=True,
                    ),
                ],
                title="Panel Stats",
            )
        ],
        id=ids.input.pv.panel.stats.accordion,
        start_collapsed=True,
        style={"margin-left": "1vh", "margin-right": "1vh"},
    )
