from constants.ids import ids
from dashboard.components import *
from dashboard.figures import *


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
