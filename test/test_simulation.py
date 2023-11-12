import unittest

import data.disk_cached
from constants.containter import PVSystemData, DateTimeRange, Location
from simulation import simulate

class SimulationTestCase(unittest.TestCase):
    def setUp(self):
        self.location = Location()
        self.pv_system_data = PVSystemData()

        self.radiation = data.disk_cached.fetch_radiation(
            self.location, DateTimeRange()
        )

    def test_simulation_standalone(self):
        result = simulate(self.location, self.pv_system_data, self.radiation)
        self.assertEqual(len(result.output.dc[0]), 365*24)

    def test_simulation_callback(self):
        pass
    #additionally test various cases with bipartite etc. different parameters

if __name__ == "__main__":
    unittest.main()
