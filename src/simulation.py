from pvlib.modelchain import ModelChain, ModelChainResult
from pvlib.pvsystem import PVSystem, Array, FixedMount
from pvlib.location import Location

import current
import cached


def construct_pvsystem():
    module = cached.data.fetch_modules()[current.state.module]
    inverter = cached.data.fetch_inverters()[current.state.inverter]
    temperature_model_parameters = cached.data.cases[current.state.case]
    mount = FixedMount(
        surface_tilt=current.state.panel_tilt,
        surface_azimuth=current.state.panel_azimuth,
    )
    array = Array(
        mount=mount,
        module_parameters=module,
        temperature_model_parameters=temperature_model_parameters,
    )
    system = PVSystem(
        arrays=[array] * current.state.number_of_modules, inverter_parameters=inverter
    )
    return system


def simulate(two_side=False) -> ModelChainResult:
    location = Location(
        current.state.latitude,
        current.state.longitude,
        altitude=current.state.altitude + current.state.house_height,
    )

    system = construct_pvsystem()
    if two_side:
        for array in system.arrays[(len(system.arrays) + 1) // 2 :]:
            array.mount.surface_azimuth = (current.state.panel_azimuth + 180) % 360

    mc = ModelChain(system, location, aoi_model="physical", spectral_model="no_loss")
    mc.run_model([cached.data.radiation] * len(system.arrays))
    return mc.results
