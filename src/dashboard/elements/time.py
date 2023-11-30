from constants.containter import *
from constants.ids import ids
from dashboard.components import *


def time() -> dbc.Container:
    return dbc.Container(
        [
            dbc.Label("Simulation time", style={"margin-right": "2vh"}),
            dcc.DatePickerRange(
                id=ids.input.time,
                start_date=DateTimeRange.start,
                end_date=DateTimeRange.end,
                display_format="DD.MM.YYYY",
                min_date_allowed=datetime(2005, 1, 1),
                max_date_allowed=datetime(2020, 12, 31),
                style={
                    'fontSize': 'inherit',
                    'fontWeight': 'inherit',
                }
            ),
        ],
        fluid=True,
    )
