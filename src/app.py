import plotly.io as pio
from dash import Dash
import dash_bootstrap_components as dbc

from dashboard.layout import get_layout
from dashboard.callbacks import get_callbacks, get_background_callback_manager

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
# TODO fix progress bar (also combine optimization with their respective simulation)
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
# TODO proper readme
# TODO show stats of modules and inverters
"""
    def fetch_best_module(self) -> dict:
        best_key = ""
        best_stat = 0
        for key in self.fetch_modules():
            module = self.modules[key]
            stats = module["I_mp_ref"] * module["V_mp_ref"] / module["A_c"]
            if stats > best_stat and module["Technology"] == "Mono-c-Si":
                best_key = key
                best_stat = stats
        result = self.modules[best_key]
        result["name"] = best_key
        return result

    def fetch_fitting_inverter(self, module: dict, number_of_modules: int) -> dict:
        single_max_power = module["I_mp_ref"] * module["V_mp_ref"]
        for key in self.fetch_inverters():
            inverter = self.inverter[key]
            min_power_condition = inverter["Pso"] <= single_max_power
            max_power_condition = (
                inverter["Pdco"] >= single_max_power * number_of_modules
            )
            manufacturer_condition = "SMA" in key
            if min_power_condition and max_power_condition and manufacturer_condition:
                return inverter
"""

pio.templates.default = "plotly_white"
external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    dbc.themes.BOOTSTRAP,
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
