import numpy as np
from scipy.optimize import minimize

from data.containter import *
from simulation import simulate


def unpack_x(x: np.ndarray, pv: PV) -> tuple:  #
    tilt = pv.tilt
    azimuth = pv.azimuth
    if pv.opt_tilt:
        tilt = x[0]
    if pv.opt_azimuth:
        azimuth = x[0 + bool(pv.opt_tilt)]
    return tilt, azimuth


def cost_function(x: np.ndarray, pos: Position, pv: PV, radiation) -> float:
    pv.tilt, pv.azimuth = unpack_x(x, pv)

    result = simulate(pos, pv, radiation)
    return -result.output.ac.sum()


def initial_values_and_bounds(
    mode: OptimizationState,
    min_value: float,
    max_value: float,
    actual_min: float,
    actual_max: float,
) -> tuple:
    if mode == OptimizationState.Fix.value:
        return [], []
    elif mode == OptimizationState.Optimize.value:
        return [(actual_max + actual_min) / 2], [(actual_min, actual_max)]
    elif mode == OptimizationState.Constrain.value:
        lower_bound = min_value if min_value is not None else actual_min
        upper_bound = max_value if max_value is not None else actual_max
        return [(lower_bound + upper_bound) / 2], [(lower_bound, upper_bound)]
    else:
        raise ValueError("Invalid mode")


def optimize(pos: Position, pv: PV, radiation) -> tuple:
    init_tilt, bounds_tilt = initial_values_and_bounds(
        pv.opt_tilt,
        pv.min_tilt,
        pv.max_tilt,
        0,
        90,
    )
    init_azimuth, bounds_azimuth = initial_values_and_bounds(
        pv.opt_azimuth,
        pv.min_azimuth,
        pv.max_azimuth,
        0,
        360,
    )
    x0 = np.array(init_tilt + init_azimuth)
    bounds = bounds_tilt + bounds_azimuth

    tilt = pv.tilt
    azimuth = pv.azimuth
    if x0.size > 0:
        results = minimize(
            cost_function,
            x0,
            method="Nelder-Mead",
            bounds=bounds,
            tol=1e-1,
            args=(pos, pv, radiation),
        )
        tilt, azimuth = unpack_x(results.x, pv)

    return tilt, azimuth
