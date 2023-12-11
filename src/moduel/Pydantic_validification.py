import streamlit as st
from src.moduel.Data_Model import StandardBuildingProfileGeneralInput, StandardBuildingElectricityProfileInput, StandardBuildingHeatingProfileInput, StandardBuildingCoolingProfileInput, StandardIndustrialProfileInput, StandardLoadProfile
from pydantic import ValidationError
import json


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
            return parsed_data
        except ValidationError as e:
            raise AssertionError(f"Validation error: {e}")
    
    def validation_thermal_data(self,json_data):
        try:
            parsed_data = StandardBuildingHeatingProfileInput.parse_raw(json_data)
            return parsed_data
        except ValidationError as e:
            raise AssertionError(f"Validation error: {e}")
    
    def validation_cooling_data(self,json_data):
        try:
            parsed_data = StandardBuildingCoolingProfileInput.parse_raw(json_data)
            return parsed_data
        except ValidationError as e:
            raise AssertionError(f"Validation error: {e}")
