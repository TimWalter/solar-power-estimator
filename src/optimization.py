import numpy as np
from scipy.optimize import minimize
from pvlib.location import Location

from data.containter import *
from simulation import simulate


def unpack_x(x: np.ndarray, tilt_info: OptimizableVariable, azimuth_info:OptimizableVariable) -> tuple:  #
    tilt = tilt_info.value
    azimuth = azimuth_info.value
    if tilt_info.state != OptimizationState.Fix.value:
        tilt = x[0]
    if azimuth_info.state != OptimizationState.Fix.value:
        azimuth = x[0 + int(tilt_info.state != OptimizationState.Fix.value)]
    return tilt, azimuth


def cost_function(x: np.ndarray, pos: Location, pv: PVSystemData, radiation, tilt_info: OptimizableVariable,
                  azimuth_info: OptimizableVariable) -> float:
    pv.tilt, pv.azimuth = unpack_x(x, tilt_info, azimuth_info)

    result = simulate(pos, pv, radiation)
    return -result.output.ac.sum()


def initial_values_and_bounds(
        info: OptimizableVariable,
        actual_min: float,
        actual_max: float,
) -> tuple:
    if info.state == OptimizationState.Fix.value:
        return [], []
    elif info.state == OptimizationState.Optimize.value:
        return [(actual_max + actual_min) / 2], [(actual_min, actual_max)]
    elif info.state == OptimizationState.Constrain.value:
        lower_bound = info.min if info.min is not None else actual_min
        upper_bound = info.max if info.max is not None else actual_max
        return [(lower_bound + upper_bound) / 2], [(lower_bound, upper_bound)]
    else:
        raise ValueError("Invalid mode")


def optimize(pos: Location, pv: PVSystemData, radiation, tilt_info: OptimizableVariable,
             azimuth_info: OptimizableVariable) -> tuple:
    init_tilt, bounds_tilt = initial_values_and_bounds(tilt_info, 0, 90)
    init_azimuth, bounds_azimuth = initial_values_and_bounds(azimuth_info, 0, 360)
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
            args=(pos, pv, radiation, tilt_info, azimuth_info),
        )
        tilt, azimuth = unpack_x(results.x, tilt_info, azimuth_info)

    return tilt, azimuth
