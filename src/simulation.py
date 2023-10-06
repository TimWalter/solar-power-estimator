from pvlib.modelchain import ModelChain
from pvlib.pvsystem import PVSystem, Array, FixedMount
from pvlib.location import Location
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS

from data.containter import *
from data import ram_cached


def construct_pvsystem(pv: PV):
    module = ram_cached.fetch_modules()[pv.module]
    inverter = ram_cached.fetch_inverters()[pv.inverter]
    temperature_model_parameters = TEMPERATURE_MODEL_PARAMETERS["sapm"][pv.case]
    arrays = []
    for i in range(pv.number_of_modules):
        arrays.append(
            Array(
                mount=FixedMount(
                    surface_azimuth=pv.azimuth,
                    surface_tilt=pv.tilt,
                ),
                module_parameters=module,
                temperature_model_parameters=temperature_model_parameters,
            )
        )
    system = PVSystem(
        arrays=arrays, inverter_parameters=inverter
    )
    return system


def simulate(
    pos: Position, roof: Roof, pv: PV, radiation, two_side: bool = False
) -> Result:
    location = Location(
        pos.latitude,
        pos.longitude,
        altitude=pos.altitude + roof.height,
    )

    system = construct_pvsystem(pv)
    if two_side:
        for array in system.arrays[(len(system.arrays) + 1) // 2 :]:
            array.mount.surface_azimuth = (pv.azimuth + 180) % 360

    mc = ModelChain(system, location, aoi_model="physical", spectral_model="no_loss")
    mc.run_model([radiation] * len(system.arrays))
    return Result(mc.results, pv.tilt, pv.azimuth)
