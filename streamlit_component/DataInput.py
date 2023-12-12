import numpy as np
import pandas as pd
import streamlit as st
import json

from src.moduel.Data_Model import *
from src.moduel.DataFileImporter import readCSVasDataFrame as readCSV
from src.moduel.ProfileRunner import (map_building_calss_to_demandlib,
                                      map_subsector_to_demandlib,
                                      map_wind_calss_to_demandlib)
from src.moduel.Visualizer import DataVisualizer


class GeneralDataInputBuilding:
    def run_general_data_input(self,):
        st.subheader("General input")
        self.handle_simulation_year()
        self.handle_temperature_input()

    def handle_simulation_year(self,):
        self.simulation_year_coloumn, self.temperature_file_coloumn = st.columns(2)
        with self.simulation_year_coloumn:
            self.simulation_year = st.number_input("Simulation year:", 2000, 2100, 2023, key="unique_key_value1")
        
    def handle_temperature_input(self,):
        with self.temperature_file_coloumn:
            options = ["Use existing temperature file", "Enter temperature data"]
            use_existing_temperature_file = st.radio("Temperature data:", options)
            if use_existing_temperature_file == "Use existing temperature file":
                filename_temperature = "temperature.csv"
                self.temperature = readCSV(filename_temperature)["temperature"]
            else:
                st.write('For more information about the format of the CSV file please check the expander below')
                with st.expander("CSV File Format"):
                    st.write('The CSV file must have either two columns named "time" and "temperature" or a single column named "temperature". The temperature must be hourly for exactly one year(8760 hours), more raws is not accepted.The file should be in plain text format with a .csv extension, and the column name(s) should be included in the first row of the file.')
            # User enters temperature data
                temperature_input = st.container()
                with temperature_input:
                    st.write('Please enter temperature data')
                    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
                    if uploaded_file is not None:
                        self.temperature = pd.read_csv(uploaded_file)["temperature"] 
                    else:
                        st.write("No file uploaded")
        
    def json(self):
        obj = StandardBuildingProfileGeneralInput(temperature=self.temperature, simulation_year=self.simulation_year)
        data = {
            "simulation_year": obj.simulation_year,
        }
        return json.dumps(data)
            
class ElectricalInput:
    def run_electrical_input(self,):
        st.subheader("Input for the electrical energy demand")
        self.handle_sector_input()
        self.handle_annual_demand_input()

    def handle_sector_input(self,):
        sector_name_el, subsector_name_el = st.columns(2)
        with sector_name_el:
            options = [e.value for e in list(StandardBuildingElectricitySector)]
            self.sector  = st.selectbox('Demand sector:', options)

        with subsector_name_el:
            if self.sector == StandardBuildingElectricitySector.Residential:
                options = [e.value for e in list(StandardBuildingElectricityResidentialSubSector)]
            if self.sector == StandardBuildingElectricitySector.Agricultural:
                options = [e.value for e in list(StandardBuildingElectricityAgriculturalSubSector)]
            if self.sector == StandardBuildingElectricitySector.Agricultural:
                options = [e.value for e in list(StandardBuildingElectricityAgriculturalSubSector)]
            self.subsector_name = st.selectbox('Sub-sector:', options)
            subsector = map_subsector_to_demandlib()
            self.subsector = subsector[self.subsector_name]

    def handle_annual_demand_input(self,):
        annual_demand_elc  = st.container()
        with annual_demand_elc:
            self.annual_demand = st.number_input('Annual electrical demand in MWh:', 0.0, 20000.0, 80.0, 0.01, key="unique_key_value_2") *1000

    def json(self,):
        #electrical_data_json = StandardBuildingElectricityProfileInput(sector=self.sector, subsector=self.subsector, subsector_name=self.subsector_name, annual_demand=self.annual_demand)
        #json_electrical_data = electrical_data_json.json()
        electrical_data_json = {
            "sector": self.sector,
            "subsector_name": self.subsector_name,
            "annual_demand": self.annual_demand,
        }
        json_electrical_data = json.dumps(electrical_data_json)
        return json_electrical_data

class ThermalInput:
    def run_thermal_input(self,):
        st.subheader("Input for the thermal energy demand")
        self.handle_sector_input()
        self.handle_wind_building_class_input()
        self.handle_annual_demand_input()
        self.handle_hwd_input()
        self.handle_slp_input()

    def handle_sector_input(self,):
        sector_name_th, subsector_name_th = st.columns(2)
        with sector_name_th:
            options = [e.value for e in list(StandardBuildingHeatingSector)]
            self.sector = st.selectbox('Demand sector:', options)

        with subsector_name_th:
            if self.sector == StandardBuildingHeatingSector.Residential:
                options = [e.value for e in list(StandardBuildingHeatingResidentialSubSector)]
            if self.sector == StandardBuildingHeatingSector.Commercial:
                options = [e.value for e in list(StandardBuildingHeatingCommercialSubSector)]
            self.subsector_name = st.selectbox('Demand sector:', options)
            subsector_dict = map_subsector_to_demandlib()
            self.subsector = subsector_dict[self.subsector_name]

    def handle_annual_demand_input(self,):
        annual_demand_elc  = st.container()
        with annual_demand_elc:
            self.annual_demand = st.number_input('Annual thermal demand in MWh:', 0.0, 20000.0, 80.0, 0.01, key="unique_key_value_3") *1000

    def handle_wind_building_class_input(self,):
        wind_class, building_class = st.columns(2)
        with wind_class:
            if self.sector == StandardBuildingHeatingSector.Residential:
                options = [e.value for e in list(StandardBuildingHeatingWindClass)]
                self.wind_class_name  = st.selectbox('Wind class:', options)
                wind_class_dict = map_wind_calss_to_demandlib()
                self.wind_class = wind_class_dict[self.wind_class_name]
            else:
                self.wind_class_name = 'Windy area'
                self.wind_class = 0

        with building_class:
            if self.sector == StandardBuildingHeatingSector.Residential:
                options = [e.value for e in list(StandardBuildingHeatingAgeClass)]
                self.building_class_name = st.selectbox('Wind class:', options)
                building_class = map_building_calss_to_demandlib()
                self.building_class = building_class[self.building_class_name]
            else:
                self.building_class_name.building_class_name = 'Before_1973'
                self.building_class = 0

    def handle_hwd_input(self,):
        if self.sector == StandardBuildingHeatingSector.Residential:
            checkbox_value = st.checkbox("Hot water included?", key="unique_key_value_30")
            if checkbox_value:
                self.hwd_include = True
            else:
                self.hwd_include = False
        else:
            self.hwd_include = False

    def handle_slp_input(self,):
        if self.hwd_include == True:
            def initialize_rows():
                return np.random.randint(0, 100, size=(1, 24))
            if self.sector == StandardBuildingHeatingSector.Residential:
                checkbox_value_SLP = st.checkbox(" Insert standard load profiles for plug loads", key="unique_key_value_3470")
                if checkbox_value_SLP:
                    self.slp = True
                    st.subheader("Standard load profiles for domestic hot water demand")
                    st.write('Please scroll the data editor table to the right to fill all 24-hour data')
                    data = pd.DataFrame(columns=[f"Column {i+1}" for i in range(24)], index=[0])
                    st.write('Please enter the data for weekdays:')
                    for _ in data.columns:
                        data_workday = pd.DataFrame(initialize_rows(), columns=[f"{i+1}" for i in range(24)])
                    workday = st.data_editor(data_workday, key="unique_key_value_500", hide_index=True, )
                    data_workday = np.array(workday, dtype=np.int64) 

                    st.write('Please enter the data for saturdays:')
                    for _ in data.columns:
                        data_saturday = pd.DataFrame(initialize_rows(), columns=[f"{i+1}" for i in range(24)])
                    saturday = st.data_editor(data_saturday, key="unique_key_value_509", hide_index=True,)
                    data_saturday = np.array(saturday, dtype=np.int64)  

                    st.write('Please enter the data for sundays and holidays:')
                    for _ in data.columns:
                        data_sunday = pd.DataFrame(initialize_rows(), columns=[f"{i+1}" for i in range(24)])
                    sunday = st.data_editor(data_sunday, key="unique_key_value_519", hide_index=True,)
                    data_sunday = np.array(sunday, dtype=np.int64)  

                    StandardBuildingHeatingProfileInput.dict_days = {
                        'Monday': data_workday/100,
                        'Tuesday': data_workday/100,
                        'Wednesday': data_workday/100,
                        'Thursday': data_workday/100,
                        'Friday': data_workday/100,
                        'Saturday': data_saturday/100,
                        'Sunday': data_sunday/100,
                    }
                    self.dict_days = StandardBuildingHeatingProfileInput.dict_days
                    Visualizer = DataVisualizer()
                    Visualizer.bar_chart(data_workday, data_saturday, data_sunday, names=['Working day', 'Saturday', 'Sunday'])
                else:
                    self.dict_days = None
                    self.slp= False
        else:
            self.slp  = False
            self.dict_days = None
            
    def json(self,):
        json_thermal_data = {
            "sector": self.sector,
            "subsector_name": self.subsector_name,
            "wind_class_name": self.wind_class_name,
            "building_class_name": self.building_class_name,
            "annual_demand": self.annual_demand,
            "hwd_include": self.hwd_include,
            "slp": self.slp,
        }
        return json.dumps(json_thermal_data)


class CoolingInput:
    def run_cooling_input(self,):
        st.subheader("Input for the cooling energy demand")
        self.handle_sector_annual_demand_input()
    
    def handle_sector_annual_demand_input(self,):
        sector_name_cl, annual_demand_cl = st.columns(2)
        with sector_name_cl:
            options = [e.value for e in list( StandardBuildingCoolingSector)]
            self.sector = st.selectbox('Demand sector:', options, key='keyvalue')

        with annual_demand_cl:
            self.annual_demand = st.number_input('Annual demand in MWh:', 0.0, 10000.0, 50.0, 0.01, key="unique_key_value_6")*1000

    def json(self,):
        cooling_data_json = StandardBuildingCoolingProfileInput(sector=self.sector, annual_demand=self.annual_demand)
        json_cooling_data = cooling_data_json.json()
        return json_cooling_data
    
class GeneralDataInputIndustrial:
    def run_data_input(self,):
        st.subheader("General input")
        self.handle_simulation_year()
        self.handle_workday_input()
        self.handle_day_factor()
        self.handle_annual_demand_input()

    def handle_simulation_year(self,):
        self.simulation_year_coloumn, self.temperature_file_coloumn = st.columns(2)
        with self.simulation_year_coloumn:
            StandardIndustrialProfileInput.simulation_year = st.number_input("Simulation year:", 2000, 2100, 2023, key="unique_key_value0")
            self.simulation_year = StandardIndustrialProfileInput.simulation_year

    def handle_workday_input(self,):
        workday_beginning, workday_ending = st.columns(2)
        with workday_beginning:
            StandardIndustrialProfileInput.begginig_workday = st.number_input('Set beginning of workday:',0, 23, 8, 1)
            self.begginig_workday = StandardIndustrialProfileInput.begginig_workday
        with workday_ending:
            StandardIndustrialProfileInput.end_workday = st.number_input('Set ending of workday:',0, 23, 17, 1)
            self.end_workday = StandardIndustrialProfileInput.end_workday

    def handle_day_factor(self):
        workday_day_factor, workday_night_factor, weekend_day_factor, weekend_night_factor = st.columns(4)
        with workday_day_factor:
            StandardIndustrialProfileInput.weekday_day_factor = st.number_input('Set weekdays day factor:',0.0, 1.0, 1.0, 0.01)
            self.weekday_day_factor = StandardIndustrialProfileInput.weekday_day_factor 
        with workday_night_factor:
            StandardIndustrialProfileInput.weekday_night_factor = st.number_input('Set weekdays night factor:',0.0, 1.0, 0.8, 0.01)
            self.weekday_night_factor = StandardIndustrialProfileInput.weekday_night_factor 
        with weekend_day_factor:
            StandardIndustrialProfileInput.weekend_day_factor = st.number_input('Set weekends day factor :',0.0, 1.0, 0.0, 0.01)
            self.weekend_day_factor = StandardIndustrialProfileInput.weekend_day_factor
        with weekend_night_factor:
            StandardIndustrialProfileInput.weekend_night_factor = st.number_input('Set weekends night factor:',0.0, 1.0, 0.0, 0.01)
            self.weekend_night_factor = StandardIndustrialProfileInput.weekend_night_factor

    def handle_annual_demand_input(self,):
        annual_demand_elc , annual_demand_th = st.columns(2)
        with annual_demand_elc:
            StandardIndustrialProfileInput.annual_demand_el = st.number_input('Annual electrical demand in MWh:', 0.0, 20000.0, 80.0, 0.01, key="unique_key_value_2") *1000
            self.annual_demand_el = StandardIndustrialProfileInput.annual_demand_el 
        with annual_demand_th:
            StandardIndustrialProfileInput.annual_demand_th = st.number_input('Annual thermal demand in MWh:', 0.0, 20000.0, 80.0, 0.01, key="unique_key_value_22") *1000
            self.annual_demand_th = StandardIndustrialProfileInput.annual_demand_th
    
    def handle_json(self,):
        self.json_general_data = {"simulation_year": self.simulation_year, "begginig_workday": self.begginig_workday, "end_workday": self.end_workday, "weekday_day_factor": self.weekday_day_factor, "weekday_night_factor": self.weekday_night_factor, "weekend_day_factor": self.weekend_day_factor, "weekend_night_factor": self.weekend_night_factor, "annual_demand_el": self.annual_demand_el, "annual_demand_th": self.annual_demand_th}
        return self.json_general_data