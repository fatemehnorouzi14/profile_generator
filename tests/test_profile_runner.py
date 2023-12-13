import unittest
import os
import pandas as pd
from src.moduel.Data_Model import *
from src.moduel.ProfileRunner import (
    ProfileGeneratorElectrical,
    ProfileGeneratorThermal,
    ProfileGeneratorCooling,
)

filename_temperature = "temperature.csv"
dirname = os.getcwd()
datapath_temperature = os.path.join(dirname,'src', "resources", filename_temperature)
class TestProfileGeneratorElectrical(unittest.TestCase):
    def test_generate_electrical_load_profile(self):
        # Define your input parameters
        general_data_input = StandardBuildingProfileGeneralInput(simulation_year=2023)
        electrical_data_input = StandardBuildingElectricityProfileInput(annual_demand=1000, subsector="h0")

        # Create an instance of ProfileGeneratorElectrical
        profile_generator = ProfileGeneratorElectrical(general_data_input, electrical_data_input)

        # Call the method and check the result
        result = profile_generator.generate_electrical_load_profile()

        # Assert statements for your test
        self.assertIsInstance(result, StandardLoadProfile)
        self.assertEqual(len(result), 1, )
        self.assertTrue(all(isinstance(value, float) for value in result.value), "All values in the profile should be of type float")
        self.assertEqual(result.name, "Electrical demand")
        self.assertEqual(result.color, "green")

class TestProfileGeneratorThermal(unittest.TestCase):
    def test_generate_thermal_load_profile(self):
        # Define your input parameters
        temperature = pd.read_csv(datapath_temperature)['temperature']
        general_data_input = StandardBuildingProfileGeneralInput(simulation_year=2023, temperature=temperature)
        thermal_data_input = StandardBuildingHeatingProfileInput(
            annual_demand=2000,
            subsector="MFH",
            wind_class= 0,
            building_class= 4,
            hwd_include=True,
            dict_days=None,
            slp=False,
        )

        # Create an instance of ProfileGeneratorThermal
        profile_generator = ProfileGeneratorThermal(general_data_input, thermal_data_input)

        # Call the method and check the result
        result = profile_generator.generate_thermal_load_profile()

        # Assert statements for your test
        self.assertEqual(len(result), 3)
        for profile in result:
            self.assertIsInstance(profile, StandardLoadProfile)
            self.assertTrue(all(isinstance(value, float) for value in profile.value), "All values in the profile should be of type float")
        self.assertEqual(result[0].name, 'Total thermal demand')
        self.assertEqual(result[0].color.strip(), '#D53513')
        self.assertEqual(result[1].name, 'DHW demand')
        self.assertEqual(result[1].color.strip(), '#8D1901')
        self.assertEqual(result[2].name, 'Space heating demand')
        self.assertEqual(result[2].color.strip(), '#FB5835')

class TestProfileGeneratorCooling(unittest.TestCase):
    def test_generate_cooling_load_profile(self):
        # Define your input parameters
        temperature = pd.read_csv(datapath_temperature)['temperature']
        general_data_input = StandardBuildingProfileGeneralInput(simulation_year=2023, temperature=temperature)
        cooling_data_input = StandardBuildingCoolingProfileInput(
            annual_demand=1500,
            sector="Residential",
        )

        # Create an instance of ProfileGeneratorCooling
        profile_generator = ProfileGeneratorCooling(general_data_input, cooling_data_input)

        # Call the method and check the result
        result = profile_generator.generate_cooling_load_profile()

        # Assert statements for your test
        self.assertIsInstance(result, StandardLoadProfile)
        self.assertEqual(len(result), 1, )
        self.assertTrue(all(isinstance(value, float) for value in result.value), "All values in the profile should be of type float")
        self.assertEqual(result.name, 'Cooling demand', )
        self.assertEqual(result.color, 'blue')
        # Add more assertions as needed


