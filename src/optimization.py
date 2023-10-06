import numpy as np
from scipy.optimize import minimize

from data.containter import *
from simulation import simulate


def cost_function(
    x: np.ndarray, pos: Position, roof: Roof, pv: PV, radiation, two_side: bool
) -> float:
    pv.azimuth = x[0]
    pv.tilt = x[1]

    result = simulate(pos, roof, pv, radiation, two_side)
    return -result.output.ac.sum()


def optimize(pos: Position, roof: Roof, pv: PV, radiation, two_side: bool) -> tuple:
    results = minimize(
        cost_function,
        np.array([90, 45]),
        method="Nelder-Mead",
        bounds=[(0, 360), (roof.tilt, 90)],
        tol=1e-1,
        args=(pos, roof, pv, radiation, two_side),
    )
    return results.x
