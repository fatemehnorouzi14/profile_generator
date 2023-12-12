import streamlit as st
from src.moduel.Data_Model import StandardBuildingProfileGeneralInput, StandardBuildingElectricityProfileInput, StandardBuildingHeatingProfileInput, StandardBuildingCoolingProfileInput, StandardIndustrialProfileInput, StandardLoadProfile
from pydantic import ValidationError
import json
from src.moduel.ProfileRunner import map_subsector_to_demandlib, map_building_calss_to_demandlib, map_wind_calss_to_demandlib


class PydanticValidation:
    def validation_general_data(self,json_data):
        try:
            parsed_data = StandardBuildingProfileGeneralInput.parse_raw(json_data)
            return parsed_data
        except ValidationError as e:
            raise AssertionError(f"Validation error: {e}")

    def validation_electrical_data(self,json_data):
        try:
            parsed_data = StandardBuildingElectricityProfileInput.parse_raw(json_data)
            dict_subsector = map_subsector_to_demandlib()
            parsed_data.subsector = dict_subsector[parsed_data.subsector_name]
            return parsed_data
        except ValidationError as e:
            raise AssertionError(f"Validation error: {e}")
    
    def validation_thermal_data(self,json_data):
        try:
            parsed_data = StandardBuildingHeatingProfileInput.parse_raw(json_data)
            dict_subsector = map_subsector_to_demandlib()
            dict_building_class = map_building_calss_to_demandlib()
            dict_wind_class = map_wind_calss_to_demandlib()
            parsed_data.subsector = dict_subsector[parsed_data.subsector_name]
            parsed_data.wind_class = dict_wind_class[parsed_data.wind_class_name]
            parsed_data.building_class = dict_building_class[parsed_data.building_class_name]
            return parsed_data
        except ValidationError as e:
            raise AssertionError(f"Validation error: {e}")
    
    def validation_cooling_data(self,json_data):
        try:
            parsed_data = StandardBuildingCoolingProfileInput.parse_raw(json_data)
            return parsed_data
        except ValidationError as e:
            raise AssertionError(f"Validation error: {e}")
