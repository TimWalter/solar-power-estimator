from constants.ids import ids
from dashboard.components import *


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


def progress_bar() -> dbc.Progress:
    return dbc.Progress(id=ids.control.progress_bar, value=0)
