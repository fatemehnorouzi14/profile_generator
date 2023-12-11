import unittest

import pandas as pd

from src.demandlib.bdew.elec_slp import ElecSlp


class TestElecSlp(unittest.TestCase):

    def setUp(self):
        self.year = 2023
        self.elec_slp = ElecSlp(self.year)

    def test_create_bdew_load_profiles(self):
        slp_types = ["h0", "g0", "g1", "g2", "g3", "g4", "g5", "g6", "l0", "l1", "l2"]
        dt_index = pd.date_range(start="2023-01-01", periods=35040, freq="15Min")
        load_profiles = self.elec_slp.create_bdew_load_profiles(dt_index, slp_types)
        self.assertEqual(len(load_profiles), len(dt_index))
        self.assertEqual(len(load_profiles.columns), len(slp_types))

    def test_create_dynamic_h0_profile(self):
        dynamic_h0_profile = self.elec_slp.create_dynamic_h0_profile()
        self.assertEqual(len(dynamic_h0_profile), len(self.elec_slp.slp_frame))

    def test_get_profile(self):
        ann_el_demand_per_sector = 1000
        profile = self.elec_slp.get_profile(ann_el_demand_per_sector)
        self.assertEqual(len(profile), len(self.elec_slp.slp_frame))

if __name__ == "__main__":
    unittest.main()
