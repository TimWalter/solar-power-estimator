import numpy as np
from scipy.optimize import minimize

from simulation import simulate
import current


def cost_function(x: np.ndarray) -> float:
    current.state.panel_tilt = x[0]
    current.state.panel_azimuth = x[1]
    results = simulate()
    return -results.ac.sum()


def cost_function_two_side(x: np.ndarray) -> float:
    current.state.panel_tilt = x[0]
    current.state.panel_azimuth = x[1]
    results = simulate(True)
    return -results.ac.sum()


def optimize(two_side: bool) -> tuple:
    results = minimize(
        cost_function if not two_side else cost_function_two_side,
        np.array([45, 90]),
        method="Nelder-Mead",
        bounds=[(current.state.roof_tilt, 90), (0, 360)],
        tol=1e-1,
    )
    return results.x
