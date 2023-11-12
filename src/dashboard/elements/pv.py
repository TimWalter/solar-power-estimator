from constants.containter import *
from constants.ids import ids
from dashboard.components import *


def case_dropdown() -> dbc.Container:
    return labelled_dropdown(
        "Case",
        ids.input.pv.case,
        [case.name for case in Case],
        PVSystemData.Module.case.name,
    )


def number_of_modules_input() -> dbc.Container:
    return labelled_input(
        "Number of modules",
        ids.input.pv.number_of_modules,
        len(PVSystemData().modules),
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
