from pvlib.modelchain import ModelChain
from pvlib.pvsystem import PVSystem, Array, FixedMount
from pvlib.location import Location
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS

from constants.containter import *
from data.ram_cached import ram_cache


def construct_pvsystem(system_data: PVSystemData):
    arrays = []
    for i, module in enumerate(system_data.modules):
        panel = ram_cache.panels[module.panel.manufacturer][module.panel.series][module.panel.model]
        temperature_model_parameters = TEMPERATURE_MODEL_PARAMETERS["sapm"][module.case.value]
        arrays.append(
            Array(
                mount=FixedMount(
                    surface_azimuth=module.azimuth,
                    surface_tilt=module.tilt,
                ),
                module_parameters=panel,
                temperature_model_parameters=temperature_model_parameters,
            )
        )

    inverter = ram_cache.inverters[system_data.inverter.manufacturer][system_data.inverter.series][
        system_data.inverter.model]
    system = PVSystem(arrays=arrays, inverter_parameters=inverter)
    return system


def simulate(location: Location, pv: PVSystemData, radiation) -> Result:
    system = construct_pvsystem(pv)

    mc = ModelChain(system, location, aoi_model="physical", spectral_model="no_loss")
    mc.run_model([radiation] * len(system.arrays))
    return Result(mc.results, pv.modules[0].tilt, pv.modules[0].azimuth)
