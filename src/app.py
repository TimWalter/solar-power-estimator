import os
import plotly.io as pio
from dash import Dash, CeleryManager, DiskcacheManager
from dash_bootstrap_components import themes

from dashboard.layout import get_layout
from dashboard.callbacks import get_callbacks

# TODO nicer map with zoom, compass etc.as connect to map?
# TODO select place by map

# TODO wrap the site to not have to scroll?

# TODO introduce a rotational panel that is optimized for every hour to perfectly follow the sun
# TODO allow the insertion of demand curves to adapt yield onto demand


# TODO accordion for setup? pagination? input groups?
# TODO use dbc progress instead of custom same for loading, same for table
# TODO Add validation and remove type constraints to get rid of increment stuff

# TODO consistent documentation
# TODO proper readme

# TODO overhaul inverter and panel to split into manufacturers etc and give custom option
# TODO introduce other library
# TODO show stats of modules and inverters
# TODO make  searching for them  easier also more modules? also custom modules etc. where you just give stats

# TODO allow save/caching of various results
# TODO allow comparison of different runs
# TODO refactor (especially elements), also ids (group them), elements come with callbacks
# TODO instead of initial collapse state do not prevent initial callback

if "REDIS_URL" in os.environ:
    # Use Redis & Celery if REDIS_URL set as an env variable
    from celery import Celery

    celery_app = Celery(
        __name__, broker=os.environ["REDIS_URL"], backend=os.environ["REDIS_URL"]
    )
    background_callback_manager = CeleryManager(celery_app)
else:
    # Diskcache for non-production apps when developing locally
    import diskcache

    cache = diskcache.Cache("./cache")
    background_callback_manager = DiskcacheManager(cache)

pio.templates.default = "plotly_white"

app = Dash(
    __name__,
    external_stylesheets=[
        themes.BOOTSTRAP,
    ],
    background_callback_manager=background_callback_manager,
)

app.layout = get_layout()

if __name__ == "__main__":
    get_callbacks(app)
    app.run(debug=True)
