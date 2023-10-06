import plotly.io as pio
from dash import Dash
import dash_bootstrap_components as dbc

from dashboard.layout import get_layout
from dashboard.callbacks import get_callbacks, get_background_callback_manager

import current
import cached

# TODO nicer map with zoom, compass etc.as connect to map?
# TODO refactor to separate dashboard and simulation, constants (dashboard/simulation also in folders)
# TODO wrap the site to not have to scroll
# TODO consistent nomenclature e.g. tilt/elevation etc.
# TODO make state include pvSystem/ also location etc?
# TODO sync plots
# TODO caching all
# TODO refactor plotting and elements to make more sense
# TODO checkbox for given 2 sided for given setup
# TODO checkbox for optimization
# TODO select place by map
# TODO FASTER website
# TODO introduce a rotational panel that is optimized for every hour to perfectly follow the sun
# TODO consistent order of parameters (longitude, latitude)
# TODO faster simulation by direct caching of request results in python
# TODO checkbox for which parameters shall be fixed for optimization (azimuth or tilt) in gneeral optimization shall be customizalbe
# TODO fix progress bar
# TODO subclasses for simulationconfig for house and panel
# TODO reorder state parameters to match layout
# TODO ADD bootstrap theme (dark mode?)
# TODO combine buttons and make cancel button dbc fade
# TODO replace px with vh
# TODO make layout pretty again
# TODO add caching (gotta have input parameters again)
# TODO consistent documentation
# TODO fix all project errors
# TODO overhall optimization, choice of one-sided or two-sided not both all the time etc.

pio.templates.default = "plotly_white"
external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    dbc.themes.BOOTSTRAP
]

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    background_callback_manager=get_background_callback_manager(),
)

app.layout = get_layout()

if __name__ == "__main__":
    get_callbacks(app)
    app.run(debug=True)
