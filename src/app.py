import os
import plotly.io as pio
from dash import Dash, CeleryManager, DiskcacheManager
from dash_bootstrap_components import themes, icons

from dashboard.layout import get_layout
import dashboard.callbacks.input as ci
import dashboard.callbacks.control as cc
import dashboard.callbacks.output as co

ci.no_import_removal()
cc.no_import_removal()
co.no_import_removal()

# TODO 1. Nicer layout
# TODO 2. Tests
# TODO 3. Validation

# TODO nicer map with zoom, compass etc.as connect to map? (movable point and than just translate its location)
# TODO select place by map

# TODO wrap the site to not have to scroll?

# TODO introduce a rotational panel that is optimized for every hour to perfectly follow the sun
# TODO allow the insertion of demand curves to adapt yield onto demand

# TODO Add validation and remove type constraints to get rid of increment stuff

# TODO consistent documentation
# TODO proper readme

# TODO allow save/caching of various results
# TODO allow comparison of different runs
# TODO instead of initial collapse state do not prevent initial callback
# TODO reintroduce roof height, for pvsystem


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
    external_stylesheets=[themes.BOOTSTRAP, icons.BOOTSTRAP],
    background_callback_manager=background_callback_manager,
)

app.layout = get_layout()

if __name__ == "__main__":
    app.run(debug=True)
