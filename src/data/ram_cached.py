import json
import pvlib

from data.containter import PVSystemData, ProductIdentifier


class RAMCache:
    def __init__(self):
        self._panel = None
        self._inverter = None

    def _fetch(self, name: str) -> dict:
        internal_name = "_" + name
        if getattr(self, internal_name) is None:
            try:
                with open(f"data/{name}_database.json", "r") as file:
                    setattr(self, internal_name, json.load(file))
            except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
                raise e
        return getattr(self, internal_name)

    @property
    def panels(self) -> dict:
        return self._fetch("panel")

    @property
    def inverters(self) -> dict:
        return self._fetch("inverter")

    def _save(self, name: str, product_identifier: ProductIdentifier, data: dict):
        database = self._fetch(name)
        try:
            database[product_identifier.manufacturer][product_identifier.series][product_identifier.model]
        except KeyError:
            if product_identifier.manufacturer not in database:
                database[product_identifier.manufacturer] = {}
            if product_identifier.series not in database[product_identifier.manufacturer]:
                database[product_identifier.manufacturer][product_identifier.series] = {}

            database[product_identifier.manufacturer][product_identifier.series][product_identifier.model] = data
            with open(f"data/{name}_database.json", "w") as file:
                json.dump(database, file, indent=4)

    def save_panel(self, panel: PVSystemData.Module.Panel):
        i_l_ref, i_o_ref, r_s, r_sh_ref, a_ref, adjust = pvlib.ivtools.sdm.fit_cec_sam(*panel.stats)
        data = {
            **panel.stats.to_cec(),
            "I_L_ref": i_l_ref,
            "I_o_ref": i_o_ref,
            "R_s": r_s,
            "R_sh_ref": r_sh_ref,
            "a_ref": a_ref,
            "Adjust": adjust,
        }
        self._save("panel", panel, data)

    def save_inverter(self, inverter: PVSystemData.Inverter):
        self._save("inverter", inverter, inverter.stats.to_cec())


ram_cache = RAMCache()
