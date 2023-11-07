import unittest

from simulation import simulate
from constants.containter import PVSystemData, DateTimeRange, Location
import data.disk_cached


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


if __name__ == "__main__":
    unittest.main()
