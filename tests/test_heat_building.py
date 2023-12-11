import datetime
import os
import unittest

import pandas as pd

from src.demandlib.bdew.heat_building import HeatBuilding

filename_temperature = "temperature.csv"
datapath_temperature = os.path.join('src', "resources", filename_temperature)
temperature = pd.read_csv(datapath_temperature,)["temperature"]




class TestHeatBuilding(unittest.TestCase):
     def setUp(self):
         self.df_index = pd.date_range(datetime.datetime(2023, 1, 1, 0), periods=8760, freq="H")
         self.temperature_data = temperature
         self.heat_building = HeatBuilding( df_index=self.df_index,temperature=self.temperature_data ,annual_heat_demand=5000, shlp_type="EFH", building_class=1, wind_class=0, ww_incl=True)


     def test_get_sigmoid_parameters(self):
        sigmoid_parameters = self.heat_building.get_sigmoid_parameters()
        self.assertIsInstance(sigmoid_parameters, tuple)

     def test_get_weekday_parameters(self):
        weekday_parameters = self.heat_building.get_weekday_parameters()
        self.assertEqual(len(weekday_parameters), len(self.df_index))

     def test_get_bdew_profile(self):
            bdew_profile = self.heat_building.get_bdew_profile()
            self.assertEqual(len(bdew_profile), len(self.df_index))
        
            for value in bdew_profile:
                self.assertGreaterEqual(value, 0)

     def test_get_normalized_bdew_profile(self):
        normalized_bdew_profile = self.heat_building.get_normalized_bdew_profile()
        self.assertEqual(len(normalized_bdew_profile), len(self.df_index))
        
        for value in normalized_bdew_profile:
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 1)

     def test_hot_water_demand(self):
        hot_water_demand = self.heat_building.hot_water_demand()
        self.assertEqual(len(hot_water_demand), len(self.df_index))


if __name__ == "__main__":
    unittest.main()

