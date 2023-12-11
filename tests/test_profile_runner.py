import os
import unittest
from contextlib import AbstractContextManager
from typing import Any

import pandas as pd

from src.moduel.ProfileRunner import (ProfileGeneratorCooling,
                                      ProfileGeneratorElectricalResidential,
                                      ProfileGeneratorIndustrial,
                                      ProfileGeneratorThermal)


class TestProfileGeneratorElectricalResidential(unittest.TestCase):  
    def setUp(self):  
        # Set up some sample input data  
        class GeneralDataInput:  
            def __init__(self):  
                self.simulation_year = 2022  
                  
        class ElectricalDataInput:  
            def __init__(self):  
                self.annual_demand = 5000  
                self.subsector = 'h0'  
                  
        general_data_input = GeneralDataInput()  
        electrical_data_input = ElectricalDataInput()  
  
        # Instantiate the class  
        self.profile_generator = ProfileGeneratorElectricalResidential(general_data_input, electrical_data_input)  
  
    def test_generate_electrical_load_profile(self):  
        # Check that the generated profile has the expected length  
        profile_data_el = self.profile_generator.generate_electrical_load_profile()  
        self.assertEqual(len(profile_data_el), 35040, f"Expected profile length 8760, got {len(profile_data_el)}")  
  
        # Check that the generated profile has the expected sum  
        sum_value_elec = float(profile_data_el.sum()) / 4 / 1000  
        self.assertAlmostEqual(sum_value_elec, 5, places=1, msg=f"Expected sum 5 kWh, got {sum_value_elec:.1f} kWh")  
  
    def test_describe_profiles_el(self):  
        # Check that the generated profile statistics have the expected values  
        describe_elec = self.profile_generator.describe_profiles_elec()  
        self.assertEqual(describe_elec['sum'], '5.00', f"Expected sum 5.00 kWh, got {describe_elec['sum']} MWh")  
        self.assertAlmostEqual(float(describe_elec['peak']), 1.07, places=1, msg=f"Expected peak value 1,07 kW, got {describe_elec['peak']} kW")  
        self.assertGreater(float(describe_elec['mean']), 0.56, f"Expected mean value > 0,57, got {describe_elec['mean']}")  
        self.assertGreater(float(describe_elec['min']), 0.18, f"Expected min value > 0.19, got {describe_elec['min']}")  
    


  
class TestProfileGeneratorThermal(unittest.TestCase):  
    def setUp(self):  
        # Set up some sample input data  
        filename_temperature = "temperature.csv"
        dirname = os.getcwd()
        datapath_temperature = os.path.join(dirname,'src', "resources", filename_temperature)
        class GeneralDataInput:  
            def __init__(self):  
                self.simulation_year = 2022  
                self.temperature = pd.read_csv(datapath_temperature)['temperature']
                  
        class ThermalDataInput:  
            def __init__(self):  
                self.annual_demand = 10000  
                self.subsector = 'EFH'
                self.building_class = 4 
                self.wind_class = 0
                self.hwd_include = True  
                self.dict_days = None  
                self.slp = False  
                  
        general_data_input = GeneralDataInput()  
        thermal_data_input = ThermalDataInput()  
  
        # Instantiate the class  
        self.profile_generator = ProfileGeneratorThermal(general_data_input, thermal_data_input)  
  
    def test_generate_thermal_load_profiles(self):  
        # Check that the generated profiles have the expected length and shape  
        if self.profile_generator.hot_water_include == True:  
            profile_data_th_total, profile_data_th_space, profile_data_th_hwd = self.profile_generator.generate_thermal_load_profiles()  
            self.assertEqual(len(profile_data_th_total), 8760, f"Expected profile length 8760, got {len(profile_data_th_total)}")  
            self.assertEqual(len(profile_data_th_space), 8760, f"Expected profile length 8760, got {len(profile_data_th_space)}")  
            self.assertEqual(len(profile_data_th_hwd), 8760, f"Expected profile length 8760, got {len(profile_data_th_hwd)}")  
            self.assertEqual(profile_data_th_total.shape, profile_data_th_space.shape, "Expected space heating and total profiles to have the same shape")  
            self.assertEqual(profile_data_th_hwd.shape[1], 1, "Expected hot water profile to have one column")  
  
        else:  
            profile_data_th_total = self.profile_generator.generate_thermal_load_profiles()  
            self.assertEqual(len(profile_data_th_total), 8760, f"Expected profile length 8760, got {len(profile_data_th_total)}")  
            self.assertEqual(profile_data_th_total.shape[1], 1, "Expected total profile to have one column")  
  
    def test_describe_profiles_th(self):  
        # Check that the generated profile statistics have the expected values  
        if self.profile_generator.hot_water_include == True:  
            describe_th_total, describe_th_space, describe_th_hwd = self.profile_generator.describe_profiles_th()  
            self.assertAlmostEqual(float(describe_th_total['sum']), 10, places=1, msg=f"Expected sum 10 MWh, got {describe_th_total['sum']} MWh")  
            self.assertGreater(float(describe_th_total['peak']), 0, f"Expected peak value > 0, got {describe_th_total['peak']}")  
            self.assertGreater(float(describe_th_total['mean']), 0, f"Expected mean value > 0, got {describe_th_total['mean']}")  
            self.assertGreater(float(describe_th_total['min']), 0, f"Expected min value > 0, got {describe_th_total['min']}")  
            self.assertGreater(float(describe_th_space['peak']), 0, f"Expected peak value > 0, got {describe_th_space['peak']}")  
            self.assertGreater(float(describe_th_space['mean']), 0, f"Expected mean value > 0, got {describe_th_space['mean']}")  
           

  
class TestProfileGeneratorCooling(unittest.TestCase):  
    def setUp(self):  
        # Set up some sample input data  
        class GeneralDataInput:  
            def __init__(self):  
                self.simulation_year = 2022  
                  
        class CoolingDataInput:  
            def __init__(self):  
                self.annual_demand = 5000  
                self.sector = 'Residential'  
                  
        general_data_input = GeneralDataInput()  
        cooling_data_input = CoolingDataInput()  
  
        # Instantiate the class  
        self.profile_generator = ProfileGeneratorCooling(general_data_input, cooling_data_input)  
  
    def test_generate_cooling_load_profiles(self):  
        # Check that the generated profile has the expected length and shape  
        profile_data_cooling = self.profile_generator.generate_cooling_load_profiles()  
        self.assertEqual(len(profile_data_cooling), 8760, f"Expected profile length 8760, got {len(profile_data_cooling)}")  
        self.assertEqual(profile_data_cooling.shape[1], 1, "Expected profile to have one column")  
  
    def test_describe_profiles_cooling(self):  
        # Check that the generated profile statistics have the expected values  
        describe_cooling = self.profile_generator.describe_profiles_cooling()  
        self.assertAlmostEqual(float(describe_cooling['sum']), 5, places=1, msg=f"Expected sum 5 MWh, got {describe_cooling['sum']} MWh")  
        self.assertGreater(float(describe_cooling['peak']), 0, f"Expected peak value > 0, got {describe_cooling['peak']}")  
        self.assertGreater(float(describe_cooling['mean']), 0, f"Expected mean value > 0, got {describe_cooling['mean']}")  
        self.assertGreaterEqual(float(describe_cooling['min']), 0, f"Expected min value > 0, got {describe_cooling['min']}")




class TestProfileGeneratorIndustrial(unittest.TestCase):
    def setUp(self):
        class GeneralDataInput:  
            def __init__(self):  
                self.simulation_year = 2022 
                self.begginig_workday = 8
                self.end_workday = 16
                self.weekday_day_factor = 1
                self.weekday_night_factor = 0.8
                self.weekend_day_factor = 0
                self.weekend_night_factor = 0
        class ElectricalDataInput:
            def __init__(self):  
                self.annual_demand = 5000
        class ThermalDataInput:
            def __init__(self):  
                self.annual_demand = 5000
                
        general_data_input = GeneralDataInput()
        electrical_data_input = ElectricalDataInput()
        thermal_data_input = ThermalDataInput()
        self.profile_generator = ProfileGeneratorIndustrial(general_data_input, electrical_data_input, thermal_data_input)

    def test_generate_industrial_load_profile(self):  
        profile_industrial_elec= self.profile_generator.generate_electrical_load_profile()
        profile_industrial_th= self.profile_generator.generate_thermal_load_profile()  
        self.assertEqual(len(profile_industrial_elec), 8760*4, f"Expected profile length 35040, got {len(profile_industrial_elec)}") 
        self.assertEqual(len(profile_industrial_th), 8760*4, f"Expected profile length 35040, got {len(profile_industrial_th)}") 


if __name__ == '__main__':
    unittest.main()
