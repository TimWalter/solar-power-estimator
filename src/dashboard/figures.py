from typing import List, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from dash.dash_table.Format import Format, Scheme, Symbol

from data.containter import *
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


def progress_figure(progress):
    progress_graph = go.Figure(
        data=[
            go.Bar(
                x=[progress],
                orientation="h",
                width=3,
                base=0.5,
                marker={"color": "rgba(20,125,174,255)"},
            ),
        ],
        layout={
            "xaxis": {
                "range": [0, 3.5],
                "tickmode": "array",
                "tickvals": np.array(range(4)) + 0.5,
                "ticktext": [
                    "Start",
                    "Fetch Data",
                    "Optimization",
                    "Simulation",
                ],
                "zeroline": False,
            },
            "yaxis": {"showticklabels": False, "visible": False},
            "title": {"text": "Progress", "y": 0.5, "x": 0.03, "xanchor": "left"},
            "margin": {"t": 20, "b": 20},
        },
    )
    return progress_graph


def get_table_columns(pv: PV) -> list:
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
    if pv.opt_tilt != OptimizationState.Fix:
        columns.append({"name": "Tilt [˚]", "format": angle_format})
    if pv.opt_azimuth != OptimizationState.Fix:
        columns.append({"name": "Azimuth [˚]", "format": angle_format})
    if pv.bipartite:
        columns.append({"name": f"1. Side - Total DC [kWh]", "format": power_format})
        columns.append({"name": f"2. Side - Total DC [kWh]", "format": power_format})
        columns.append({"name": f"1. Side - DC/Panel [kWh]", "format": power_format})
        columns.append({"name": f"2. Side - DC/Panel [kWh]", "format": power_format})

    columns = [
        {"name": col["name"], "id": col["name"], "format": col["format"], "type": "numeric"}
        for col in columns
    ]

    return columns


def get_table_data(pv: PV, result: Result) -> List[dict]:
    columns = get_table_columns(pv)
    show_tilt = pv.opt_tilt != OptimizationState.Fix
    show_azimuth = pv.opt_azimuth != OptimizationState.Fix
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
                np.sum([r["p_mp"].sum() for r in result.output.dc[pv.side1 :]]) / 1000
            )
        elif i == 4 + show_tilt + show_azimuth and pv.bipartite:
            data[col["name"]] = (
                np.sum([r["p_mp"].sum() for r in result.output.dc[: pv.side1]])
                / pv.side1
                / 1000
            )
        elif i == 5 + show_tilt + show_azimuth and pv.bipartite:
            data[col["name"]] = (
                np.sum([r["p_mp"].sum() for r in result.output.dc[pv.side1 :]])
                / pv.side2
                / 1000
            )

    return [data]


def get_graph_figure(pv: PV, result: Result = None) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(AC_figure(result))
    fig.add_trace(DC_figure(result))
    fig.add_trace(AC_minus_DC_figure(result))
    if pv.bipartite:
        fig.add_trace(side1_figure(pv, result))
        fig.add_trace(side2_figure(pv, result))
        fig.add_trace(bipartite_differential_figure(pv, result))

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


def side1_figure(pv: PV, result: Result = None) -> go.Scatter:
    return go.Scatter(
        x=result.output.times if result is not None else [0],
        y=np.sum([r["p_mp"] for r in result.output.dc[: pv.side1]], axis=0)
        / pv.side1
        / 1000
        if result is not None
        else [0],
        name="1. Side / Panel",
        opacity=0.75,
        visible="legendonly",
    )


def side2_figure(pv: PV, result: Result = None) -> go.Scatter:
    return go.Scatter(
        x=result.output.times if result is not None else [0],
        y=np.sum([r["p_mp"] for r in result.output.dc[pv.side1 :]], axis=0)
        / pv.side2
        / 1000
        if result is not None
        else [0],
        name="2. Side / Panel",
        opacity=0.75,
        visible="legendonly",
    )


def bipartite_differential_figure(pv: PV, result: Result = None) -> go.Scatter:
    return go.Scatter(
        x=result.output.times if result is not None else [0],
        y=np.sum([r["p_mp"] for r in result.output.dc[: pv.side1]], axis=0)
        / pv.side1
        / 1000
        - np.sum([r["p_mp"] for r in result.output.dc[pv.side1 :]], axis=0)
        / pv.side2
        / 1000
        if result is not None
        else [0],
        name="1. Side / Panel - 2. Side / Panel",
        opacity=0.75,
        visible="legendonly",
    )
