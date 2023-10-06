from typing import List, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from dash.dash_table.Format import Format, Scheme, Symbol

from data.containter import *
from sec.keys import MAPBOX_API_KEY


def map_figure(pos: Position) -> go.Figure:
    fig = go.Figure(
        go.Scattermapbox(
            lat=[pos.latitude],
            lon=[pos.longitude],
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
                "lon": pos.longitude,
                "lat": pos.latitude,
            },
            "zoom": 12.5,
        },
        margin={
            "b": 10,
            "t": 32,
            "l": 25,
            "r": 0,
        },  # Set the bottom margin to zero to reduce space
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
                "range": [0, 6],
                "tickmode": "array",
                "tickvals": np.array(range(7)) + 0.5,
                "ticktext": [
                    "Start",
                    "Fetch Data",
                    "1. Simulation",
                    "1. Optimization",
                    "2. Simulation",
                    "2. Optimization",
                    "3. Simulation",
                ],
                "zeroline": False,
            },
            "yaxis": {"showticklabels": False, "visible": False},
            "title": {"text": "Progress", "y": 0.5, "x": 0.03, "xanchor": "left"},
            "margin": {"t": 20, "b": 20},
        },
    )
    return progress_graph


def get_empty_table() -> Tuple[pd.DataFrame, list]:
    columns = [
        "",
        "Tilt [°]",
        "Azimuth [°]",
        "Total AC [kW/h]",
        "Total DC [kW/h]",
        "DC/Panel [kW/h]",
    ]
    row_descriptions = ["Manual", "One-sided Optimal", "Two-sided Optimal"]
    data = [{"": row} for row in row_descriptions]

    data = pd.DataFrame(data=data, columns=columns)

    angle_format = Format(
        precision=2, scheme=Scheme.fixed, symbol=Symbol.yes, symbol_suffix="˚"
    )
    power_format = Format(
        precision=2, scheme=Scheme.fixed, symbol=Symbol.yes, symbol_suffix=" kW/h"
    )
    columns = [{"name": i, "id": i, "type": "numeric"} for i in columns]
    columns[1]["format"] = angle_format
    columns[2]["format"] = angle_format
    columns[3]["format"] = power_format
    columns[4]["format"] = power_format
    columns[5]["format"] = power_format

    return data, columns


def get_table_data(result: Result, result_1s: Result, result_2s: Result) -> List[dict]:
    table_data, _ = get_empty_table()
    table_data["Tilt [°]"] = [
        result.tilt,
        result_1s.tilt,
        result_2s.tilt,
    ]
    table_data["Azimuth [°]"] = [
        result.azimuth,
        result_1s.azimuth,
        result_2s.azimuth,
    ]
    table_data["Total AC [kW/h]"] = [
        result.output.ac.sum() / 1000,
        result_1s.output.ac.sum() / 1000,
        result_2s.output.ac.sum() / 1000,
    ]
    table_data["Total DC [kW/h]"] = [
        np.sum([r["p_mp"].sum() for r in result.output.dc]) / 1000,
        np.sum([r["p_mp"].sum() for r in result_1s.output.dc]) / 1000,
        np.sum([r["p_mp"].sum() for r in result_2s.output.dc]) / 1000,
    ]
    table_data["DC/Panel [kW/h]"] = [
        result.output.dc[0]["p_mp"].sum() / 1000,
        result_1s.output.dc[0]["p_mp"].sum() / 1000,
        (result_2s.output.dc[0]["p_mp"].sum() + result_2s.output.dc[-1]["p_mp"].sum())
        / 2000,
    ]
    return table_data.to_dict("records")


def plot_results(x, data: list, names: list, title: str, non_visible_indices: list):
    fig = go.Figure()
    for i, (d, n) in enumerate(zip(data, names)):
        fig.add_trace(
            go.Scatter(
                x=x,
                y=d,
                name=n,
                opacity=0.5,
                visible="legendonly" if i in non_visible_indices else True,
            )
        )

    fig.update_layout(
        title=dict(text=title, y=0.9, x=0.5, xanchor="center", yanchor="top"),
        legend=dict(
            orientation="h",
            yanchor="top",
            xanchor="right",
            y=1.2,
            x=1,
            bgcolor="rgba(0, 0, 0, 0)",  # Transparent background
        ),
        yaxis_title="Power [W/h]",
    )

    return fig


def fig1(result: Result) -> go.Figure:
    result_dc = np.sum([r["p_mp"] for r in result.output.dc], axis=0)
    return plot_results(
        result.output.times,
        [
            result.output.ac,
            result_dc,
            result_dc - result.output.ac,
        ],
        [f"Manual (AC)", f"Manual (DC)", f"Differential (DC-AC)"],
        "Manual Power Output",
        [2],
    )


def fig2(result: Result, result_1s: Result, result_2s: Result) -> go.Figure:
    max_output = (
        result_1s.output.ac
        if result_1s.output.ac.sum() > result_2s.output.ac.sum()
        else result_2s.output.ac
    )
    return plot_results(
        result.output.times,
        [
            result.output.ac,
            result_1s.output.ac,
            result_2s.output.ac,
            max_output - result.output.ac,
        ],
        [
            f"Manual (AC)",
            f"One-sided Optimal (AC)",
            f"Two-sided Optimal (AC)",
            "Differential Max - Manual (AC)",
        ],
        "Comparative Power Output",
        [0, 1, 2],
    )


def fig3(result: Result, result_1s: Result, result_2s: Result) -> go.Figure:
    return plot_results(
        result.output.times,
        [
            result.output.dc[0]["p_mp"],
            result_1s.output.dc[0]["p_mp"],
            result_2s.output.dc[0]["p_mp"],
            result_2s.output.dc[-1]["p_mp"],
            result_1s.output.dc[0]["p_mp"] - result.output.dc[0]["p_mp"],
            result_1s.output.dc[0]["p_mp"]
            - (result_2s.output.dc[0]["p_mp"] + result_2s.output.dc[-1]["p_mp"]) / 2,
            result_2s.output.dc[0]["p_mp"] - result_2s.output.dc[-1]["p_mp"],
        ],
        [
            "Manual (DC)",
            "One-sided Optimal (DC)",
            "Two-sided Optimal (1st side) (DC)",
            "Two-sided Optimal (2nd side) (DC)",
            "Differential Optimal One-sided - Manual (DC)",
            "Differential One-sided - Two-sided (DC)",
            "Differential 1st side - 2nd side (DC)",
        ],
        "Power Output per Panel",
        [0, 1, 2, 3, 4, 5],
    )
