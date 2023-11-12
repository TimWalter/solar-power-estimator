from constants.ids import ids
from dashboard.components import *
from dashboard.figures import *


def name_dropdown() -> dbc.Container:
    return labelled_dropdown(
        "Location", ids.input.location.name, [Location().name], Location().name
    )


def map_graph() -> dcc.Graph:
    return dcc.Graph(
        id=ids.input.location.map,
        figure=map_figure(Location().latitude, Location().longitude),
        config={
            "autosizable": True,
            "scrollZoom": True,
            "modeBarButtonsToRemove": ["lasso2d", "select2d"],
        },
        style={
            "padding-top": "1vh",
            "padding-bottom": "1vh",
        },
        className="transparent-modebar",
    )


def latitude_input() -> dbc.Container:
    return labelled_input("Latitude", ids.input.location.latitude, Location().latitude)


def longitude_input() -> dbc.Container:
    return labelled_input(
        "Longitude", ids.input.location.longitude, Location().longitude
    )


def altitude_input() -> dbc.Container:
    return labelled_input("Altitude", ids.input.location.altitude, Location().altitude)
