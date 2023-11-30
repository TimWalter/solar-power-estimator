import dash_bootstrap_components as dbc
from dash import dcc, html

from constants.enums import OptimizationState


def labelled_dropdown(
    label: str,
    input_id: str,
    options: list,
    value: str,
    disabled: bool = False,
    store_id: str = None,
) -> dbc.Container:
    return dbc.Container(
        [
            dbc.Label(label),
            dcc.Dropdown(
                id=input_id,
                options=options,
                value=value,
                searchable=True,
                clearable=False,
                disabled=disabled,
            ),
            dcc.Store(id=store_id) if store_id else None,
        ],
        fluid=True,
        style={'marginLeft': '-1vh', 'width': '105%'}
    )


def labelled_input(
    label: str,
    input_id: str,
    initial_value: int,
    placeholder: str = None,
    input_type: str = "number",
) -> dbc.FormFloating:
    return dbc.FormFloating(
        [
            dbc.Input(
                id=input_id,
                type=input_type,
                value=initial_value,
                placeholder=placeholder,
            ),
            dbc.Label(label),
        ]
    )


def horizontal_line():
    return html.Hr(
        style={"borderTop": "0.1vh solid #888", "width": "90%", "margin": "4vh auto"}
    )


def labelled_input_group(
    symbol: list,
    description: str,
    input_id: str,
    initial_value: str,
    unit: str = None,
    type: str = "number",
    disabled=False,
) -> dbc.InputGroup:
    return dbc.InputGroup(
        [
            dbc.InputGroupText(symbol),
            dbc.FormFloating(
                [
                    dbc.Input(
                        id=input_id, type=type, value=initial_value, disabled=disabled
                    ),
                    dbc.Label(description),
                ]
            ),
            dbc.InputGroupText(unit) if unit else None,
        ],
        className="mb-3",
    )


def labelled_select_group(
    description: str,
    input_id: str,
    options: list,
    value: str,
    disabled=False,
):
    return dbc.InputGroup(
        [
            dbc.InputGroupText(description),
            dbc.Select(
                id=input_id,
                options=options,
                value=value,
                disabled=disabled,
            ),
        ],
        className="mb-3",
    )


def labelled_optimizable_number_input(
    title: str,
    radio_id: str,
    radio_value: OptimizationState,
    fix_collapse_id: str,
    fix_input_id: str,
    fix_input_value: float,
    constrain_collapse_id: str,
    constrain_min_id: str,
    constrain_min_value: float,
    constrain_max_id: str,
    constrain_max_value: float,
) -> dbc.Container:
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(dbc.Label(title), width=2),
                    dbc.Col(
                        optimization_radio(radio_id, radio_value),
                        width=6,
                    ),
                    dbc.Col(
                        [
                            collapse_input(
                                fix_input_id, fix_input_value, fix_collapse_id
                            ),
                            collapse_double_input(
                                constrain_collapse_id,
                                constrain_min_id,
                                constrain_min_value,
                                constrain_max_id,
                                constrain_max_value,
                            ),
                        ],
                        width=3,
                    ),
                ],
                justify="around",
                align="center",
            ),
        ],
        fluid=True,
    )


def optimization_radio(idx: str, state: OptimizationState) -> html.Div:
    return html.Div(
        dbc.RadioItems(
            id=idx,
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": state.name, "value": state.value}
                for state in OptimizationState
            ],
            value=state.value,
        ),
        className="radio-group",
    )


def collapse_input(input_id: str, input_value: float, collapse_id: str) -> dbc.Collapse:
    return dbc.Collapse(
        dbc.Input(
            id=input_id,
            type="number",
            value=input_value,
        ),
        collapse_id,
    )


def collapse_double_input(
    collapse_id: str,
    input1_id: str,
    input1_value: float,
    input2_id: str,
    input2_value: float,
) -> dbc.Collapse:
    return dbc.Collapse(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Input(
                            id=input1_id,
                            type="number",
                            value=input1_value,
                            placeholder="Minimum",
                        ),
                        width=6,
                    ),
                    dbc.Col(
                        dbc.Input(
                            id=input2_id,
                            type="number",
                            value=input2_value,
                            placeholder="Maximum",
                            step="any",
                        ),
                        width=6,
                    ),
                ]
            ),
        ],
        collapse_id,
    )
