from typing import List, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from dash.dash_table.Format import Format, Scheme, Symbol

import current
from sec.keys import MAPBOX_API_KEY


def map_figure() -> go.Figure:
    fig = go.Figure(
        go.Scattermapbox(
            lat=[current.state.latitude],
            lon=[current.state.longitude],
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
                "lon": current.state.longitude,
                "lat": current.state.latitude,
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


def get_table_data() -> List[dict]:
    table_data, _ = get_empty_table()
    table_data["Tilt [°]"] = [
        current.state.manual.tilt,
        current.state.opt_one_sided.tilt,
        current.state.opt_two_sided.tilt,
    ]
    table_data["Azimuth [°]"] = [
        current.state.manual.azimuth,
        current.state.opt_one_sided.azimuth,
        current.state.opt_two_sided.azimuth,
    ]
    table_data["Total AC [kW/h]"] = [
        current.state.manual.result.ac.sum() / 1000,
        current.state.opt_one_sided.result.ac.sum() / 1000,
        current.state.opt_two_sided.result.ac.sum() / 1000,
    ]
    table_data["Total DC [kW/h]"] = [
        np.sum([r["p_mp"].sum() for r in current.state.manual.result.dc]) / 1000,
        np.sum([r["p_mp"].sum() for r in current.state.opt_one_sided.result.dc]) / 1000,
        np.sum([r["p_mp"].sum() for r in current.state.opt_two_sided.result.dc]) / 1000,
    ]
    table_data["DC/Panel [kW/h]"] = [
        current.state.manual.result.dc[0]["p_mp"].sum() / 1000,
        current.state.opt_one_sided.result.dc[0]["p_mp"].sum() / 1000,
        (
            current.state.opt_two_sided.result.dc[0]["p_mp"].sum()
            + current.state.opt_two_sided.result.dc[-1]["p_mp"].sum()
        )
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


def fig1() -> go.Figure:
    result_dc = np.sum([r["p_mp"] for r in current.state.manual.result.dc], axis=0)
    return plot_results(
        current.state.manual.result.times,
        [
            current.state.manual.result.ac,
            result_dc,
            result_dc - current.state.manual.result.ac,
        ],
        [f"Manual (AC)", f"Manual (DC)", f"Differential (DC-AC)"],
        "Manual Power Output",
        [2],
    )


def fig2() -> go.Figure:
    max_output = (
        current.state.opt_one_sided.result.ac
        if current.state.opt_one_sided.result.ac.sum()
        > current.state.opt_two_sided.result.ac.sum()
        else current.state.opt_two_sided.result.ac
    )
    return plot_results(
        current.state.manual.result.times,
        [
            current.state.manual.result.ac,
            current.state.opt_one_sided.result.ac,
            current.state.opt_two_sided.result.ac,
            max_output - current.state.manual.result.ac,
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


def fig3() -> go.Figure:
    return plot_results(
        current.state.manual.result.times,
        [
            current.state.manual.result.dc[0]["p_mp"],
            current.state.opt_one_sided.result.dc[0]["p_mp"],
            current.state.opt_two_sided.result.dc[0]["p_mp"],
            current.state.opt_two_sided.result.dc[-1]["p_mp"],
            current.state.opt_one_sided.result.dc[0]["p_mp"]
            - current.state.manual.result.dc[0]["p_mp"],
            current.state.opt_one_sided.result.dc[0]["p_mp"]
            - (
                current.state.opt_two_sided.result.dc[0]["p_mp"]
                + current.state.opt_two_sided.result.dc[-1]["p_mp"]
            )
            / 2,
            current.state.opt_two_sided.result.dc[0]["p_mp"]
            - current.state.opt_two_sided.result.dc[-1]["p_mp"],
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
