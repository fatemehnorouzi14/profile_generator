import datetime
import unittest

from src.moduel import DataFileImporter
from src.moduel.CoolingProfileGenerator import (CoolingProfileGenerator,
                                                ElectricalProfileGenerator,
                                                ThermalLoadProfileGenerator)


class TestProfileGenerators(unittest.TestCase):

    def setUp(self):
        self.simulation_year = 2023
        self.annual_demand = 10000  # Adjust this value to your specific use case
        self.cooling_generator = CoolingProfileGenerator(self.simulation_year, self.annual_demand)
        self.thermal_generator = ThermalLoadProfileGenerator(self.simulation_year, "MFH", 1, 0, self.annual_demand, True)
        self.electrical_generator = ElectricalProfileGenerator(self.simulation_year, "Some Sector", self.annual_demand)

    def test_generate_load_profile_residential(self):
        load_profile = self.cooling_generator.generate_load_profile_residential()
        self.assertEqual(len(load_profile), 8760)  # Assuming hourly data for a year

    def test_generate_load_profile_commercial(self):
        load_profile = self.cooling_generator.generate_load_profile_commercial()
        self.assertEqual(len(load_profile), 8760)  # Assuming hourly data for a year

    def test_create_thermal_load_profile(self):
        thermal_profile = self.thermal_generator.create_thermal_load_profile()
        self.assertEqual(len(thermal_profile), 8760)  # Assuming hourly data for a year



    def test_create_hot_water_profile(self):
        hot_water_profile = self.thermal_generator.create_hot_water_profile()
        self.assertEqual(len(hot_water_profile), 8760)  # Assuming hourly data for a year

    def test_create_electrical_profile(self):
        electrical_profile = self.electrical_generator.create_electrical_profile()
        self.assertEqual(len(electrical_profile), 35040)  # Assuming hourly data for a year

    # def test_calculate_day_type(self):
    #     timestamp_weekend = datetime.datetime(2023, 9, 23, 12)  # A Saturday
    #     timestamp_monday = datetime.datetime(2023, 9, 25, 12)  # A Monday
    #     timestamp_weekday = datetime.datetime(2023, 9, 26, 12)  # A weekday
    #     timestamp_holiday = datetime.datetime(2023, 10, 3, 12)   # German Unity Day

    #     self.assertEqual(CoolingProfileGenerator.calculate_day_type(timestamp_weekend,self.holiday),1)
    #     self.assertEqual(CoolingProfileGenerator.calculate_day_type(timestamp_monday),2)
    #     self.assertEqual(CoolingProfileGenerator.calculate_day_type(timestamp_weekday),0)
    #     self.assertEqual(CoolingProfileGenerator.calculate_day_type(timestamp_holiday),1)

        # def test_create_space_heating_profile(self):
    #     space_heating_profile = self.thermal_generator.create_space_heating_profile()
    #     self.assertEqual(len(space_heating_profile), 8760)  # Assuming hourly data for a year


if __name__ == '__main__':
    unittest.main()
