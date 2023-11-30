from typing import List

import numpy as np
import plotly.graph_objs as go
from dash.dash_table.Format import Format, Scheme, Symbol

from constants.containter import *
from sec.keys import MAPBOX_API_KEY


def map_figure(latitude: float, longitude: float) -> go.Figure:
    fig = go.Figure(
        go.Scattermapbox(
            lat=[latitude],
            lon=[longitude],
            mode="markers",
            marker=go.scattermapbox.Marker(
                size=20,
                color="rgb(238, 38, 37)",
            ),
        )
    )
    fig.update_layout(
        mapbox={
            "accesstoken": MAPBOX_API_KEY,
            "style": "satellite-streets",
            "center": {
                "lat": latitude,
                "lon": longitude,
            },
            "zoom": 12.5,
        },
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )
    return fig

def get_table_columns(tilt_state: OptimizationState, azimuth_state: OptimizationState, bipartite: bool) -> list:
    angle_format = Format(
        precision=2, scheme=Scheme.fixed, symbol=Symbol.yes, symbol_suffix="˚"
    )
    power_format = Format(
        precision=2, scheme=Scheme.fixed, symbol=Symbol.yes, symbol_suffix=" kWh"
    )

    columns = [
        {"name": "Total AC [kWh]", "format": power_format},
        {"name": "Total DC [kWh]", "format": power_format},
    ]
    if tilt_state != OptimizationState.Fix:
        columns.append({"name": "Tilt [˚]", "format": angle_format})
    if azimuth_state != OptimizationState.Fix:
        columns.append({"name": "Azimuth [˚]", "format": angle_format})
    if bipartite:
        columns.append({"name": f"1. Side - Total DC [kWh]", "format": power_format})
        columns.append({"name": f"2. Side - Total DC [kWh]", "format": power_format})
        columns.append({"name": f"1. Side - DC/Panel [kWh]", "format": power_format})
        columns.append({"name": f"2. Side - DC/Panel [kWh]", "format": power_format})

    columns = [
        {"name": col["name"], "id": col["name"], "format": col["format"], "type": "numeric"}
        for col in columns
    ]

    return columns


def get_table_data(pv: PVSystemData, result: Result, tilt_info: OptimizableVariable,
                   azimuth_info: OptimizableVariable) -> List[dict]:
    columns = get_table_columns(tilt_info.state, azimuth_info.state, pv.bipartite)
    show_tilt = tilt_info.state != OptimizationState.Fix
    show_azimuth = azimuth_info.state != OptimizationState.Fix
    data = {}
    for i, col in enumerate(columns):
        if i == 0:
            data[col["name"]] = result.output.ac.sum() / 1000
        elif i == 1:
            data[col["name"]] = (
                    np.sum([r["p_mp"].sum() for r in result.output.dc]) / 1000
            )
        elif i == 2 and show_tilt:
            data[col["name"]] = result.tilt
        elif i == 2 + show_tilt and show_azimuth:
            data[col["name"]] = result.azimuth
        elif i == 2 + show_tilt + show_azimuth and pv.bipartite:
            data[col["name"]] = (
                    np.sum([r["p_mp"].sum() for r in result.output.dc[: pv.side1]]) / 1000
            )
        elif i == 3 + show_tilt + show_azimuth and pv.bipartite:
            data[col["name"]] = (
                    np.sum([r["p_mp"].sum() for r in result.output.dc[pv.side1:]]) / 1000
            )
        elif i == 4 + show_tilt + show_azimuth and pv.bipartite:
            data[col["name"]] = (
                    np.sum([r["p_mp"].sum() for r in result.output.dc[: pv.side1]])
                    / pv.modules[0].panel.side1
                    / 1000
            )
        elif i == 5 + show_tilt + show_azimuth and pv.bipartite:
            data[col["name"]] = (
                    np.sum([r["p_mp"].sum() for r in result.output.dc[pv.side1:]])
                    / pv.modules[0].panel.side2
                    / 1000
            )

    return [data]


def get_graph_figure(bipartite: bool, side1: int, side2: int, result: Result = None) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(AC_figure(result))
    fig.add_trace(DC_figure(result))
    fig.add_trace(AC_minus_DC_figure(result))
    if bipartite:
        fig.add_trace(side1_figure(side1, result))
        fig.add_trace(side2_figure(side1, side2, result))
        fig.add_trace(bipartite_differential_figure(side1, side2, result))

    fig.update_layout(
        # title=dict(text="", y=0.9, x=0.5, xanchor="center", yanchor="top"),
        legend=dict(
            orientation="h",
            yanchor="top",
            xanchor="right",
            y=1.2,
            x=1,
            bgcolor="rgba(0, 0, 0, 0)",  # Transparent background
        ),
        xaxis_title="Time [h]",
        yaxis_title="Power [W/h]",
    )
    return fig


def AC_figure(result: Result = None) -> go.Scatter:
    return go.Scatter(
        x=result.output.times if result is not None else [0],
        y=result.output.ac / 1000 if result is not None else [0],
        name="AC",
        opacity=0.75,
        visible=True,
    )


def DC_figure(result: Result = None) -> go.Scatter:
    return go.Scatter(
        x=result.output.times if result is not None else [0],
        y=np.sum([r["p_mp"] for r in result.output.dc], axis=0) / 1000
        if result is not None
        else [0],
        name="DC",
        opacity=0.75,
        visible="legendonly",
    )


def AC_minus_DC_figure(result: Result = None) -> go.Scatter:
    return go.Scatter(
        x=result.output.times if result is not None else [0],
        y=(result.output.ac - np.sum([r["p_mp"] for r in result.output.dc], axis=0))
          / 1000
        if result is not None
        else [0],
        name="AC - DC",
        opacity=0.75,
        visible="legendonly",
    )


def side1_figure(side1: int, result: Result = None) -> go.Scatter:
    return go.Scatter(
        x=result.output.times if result is not None else [0],
        y=np.sum([r["p_mp"] for r in result.output.dc[: side1]], axis=0)
          / side1
          / 1000
        if result is not None
        else [0],
        name="1. Side / Panel",
        opacity=0.75,
        visible="legendonly",
    )


def side2_figure(side1: int, side2: int, result: Result = None) -> go.Scatter:
    return go.Scatter(
        x=result.output.times if result is not None else [0],
        y=np.sum([r["p_mp"] for r in result.output.dc[side1:]], axis=0)
          / side2
          / 1000
        if result is not None
        else [0],
        name="2. Side / Panel",
        opacity=0.75,
        visible="legendonly",
    )


def bipartite_differential_figure(side1: int, side2: int, result: Result = None) -> go.Scatter:
    return go.Scatter(
        x=result.output.times if result is not None else [0],
        y=np.sum([r["p_mp"] for r in result.output.dc[: side1]], axis=0)
          / side1
          / 1000
          - np.sum([r["p_mp"] for r in result.output.dc[side1:]], axis=0)
          / side2
          / 1000
        if result is not None
        else [0],
        name="1. Side / Panel - 2. Side / Panel",
        opacity=0.75,
        visible="legendonly",
    )
