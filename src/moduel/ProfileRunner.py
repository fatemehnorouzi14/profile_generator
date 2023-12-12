import datetime
from datetime import time as settime

import holidays
import pandas as pd

from src.demandlib.bdew.elec_slp import ElecSlp
from src.demandlib.bdew.heat_building import HeatBuilding
from src.demandlib.particular_profiles import IndustrialLoadProfile
from src.moduel.CoolingProfileGenerator import CoolingProfileGenerator
from src.moduel.Data_Model import *


# Class for generating electrical load profiles for residential buildings
class ProfileGeneratorElectrical:
    def __init__(self, general_data_input: StandardBuildingProfileGeneralInput, electrical_data_input:StandardBuildingElectricityProfileInput):
        self.simulation_year = general_data_input.simulation_year
        self.electrical_demand =  electrical_data_input.annual_demand
        self.subsector = electrical_data_input.subsector

    def generate_electrical_load_profile(self,) -> StandardLoadProfile:
        obj_el = ElecSlp(self.simulation_year ,holidays=holidays.Germany(years = self.simulation_year))
        profile_data_el = obj_el.get_profile({self.subsector: self.electrical_demand})
        color = 'green'
        name = "Electrical demand"
        value = [profile_data_el.values]
        profile = StandardLoadProfile()
        profile.value = profile_data_el.iloc[:, 0]
        profile.name =  name
        profile.color = color
        return profile

class ProfileGeneratorThermal:
    def __init__(self, general_data_input: StandardBuildingProfileGeneralInput, thermal_data_input: StandardBuildingHeatingProfileInput):
        self.simulation_year = general_data_input.simulation_year
        self.annual_demand = thermal_data_input.annual_demand
        self.shlf_type =  thermal_data_input.subsector
        self.wind_class = thermal_data_input.wind_class
        self.building_class = thermal_data_input.building_class
        self.hot_water_include = thermal_data_input.hwd_include
        self.dict_days = thermal_data_input.dict_days
        self.slp = thermal_data_input.slp
        self.temperature = general_data_input.temperature
        dataframe = pd.DataFrame(index=pd.date_range(datetime.datetime(general_data_input.simulation_year, 1, 1, 0), periods=8760, freq="H"))
        self.df_index = dataframe.index
        self.obj_th = HeatBuilding(df_index=self.df_index, holidays=holidays.Germany(years=self.simulation_year), 
                      temperature=self.temperature, shlp_type=self.shlf_type, building_class=self.building_class, wind_class=self.wind_class, annual_heat_demand=self.annual_demand, ww_incl=self.hot_water_include, data_dict=self.dict_days)

    def generate_thermal_load_profile(self,) -> List[StandardLoadProfile]:
        if self.hot_water_include == True:
            if self.slp == True:
                profile_data_th_hwd = pd.DataFrame(self.obj_th.hot_water_demand(add_weight = True))
                profile_data_th_hwd.columns = ['temperature_geo']
                profile_data_th_hwd.index = self.df_index
                name = ['Total thermal demand', 'DHW demand', 'Space heating demand']
                color = ['#D53513 ', '#8D1901 ', '#FB5835']
                profile_data_th_total = pd.DataFrame(self.obj_th.get_bdew_profile())
                profile_data_th_space = pd.DataFrame(self.obj_th.space_heating_demand())
                profile_total = StandardLoadProfile()    
                profile_total.name =  name[0]
                profile_total.color = color[0]
                profile_total.value = profile_data_th_total.iloc[:, 0]
                profile_hwd = StandardLoadProfile()    
                profile_hwd.name =  name[1]
                profile_hwd.color = color[1]
                profile_hwd.value = profile_data_th_hwd.iloc[:, 0]
                profile_space = StandardLoadProfile()    
                profile_space.name =  name[2]
                profile_space.color = color[2]
                profile_space.value = profile_data_th_space.iloc[:, 0]

                return   profile_total, profile_hwd, profile_space
            else:
                profile_data_th_hwd = pd.DataFrame(self.obj_th.hot_water_demand())
                profile_data_th_hwd.columns = ['temperature_geo']
                profile_data_th_hwd.index = self.df_index
                name = ['Total thermal demand', 'DHW demand', 'Space heating demand']
                color = ['#D53513 ', '#8D1901 ', '#FB5835']
                profile_data_th_total = pd.DataFrame(self.obj_th.get_bdew_profile())
                profile_data_th_space = pd.DataFrame(self.obj_th.space_heating_demand())
                profile_total = StandardLoadProfile()    
                profile_total.name =  name[0]
                profile_total.color = color[0]
                profile_total.value = profile_data_th_total.iloc[:, 0]
                profile_hwd = StandardLoadProfile()    
                profile_hwd.name =  name[1]
                profile_hwd.color = color[1]
                profile_hwd.value = profile_data_th_hwd.iloc[:, 0]
                profile_space = StandardLoadProfile()    
                profile_space.name =  name[2]
                profile_space.color = color[2]
                profile_space.value = profile_data_th_space.iloc[:, 0]
                return   profile_total, profile_hwd, profile_space

        else:
            name = 'Total thermal demand'
            color = '#D53513 '
            profile_data_th_total = pd.DataFrame(self.obj_th.get_bdew_profile())
            profile_total = StandardLoadProfile()    
            profile_total.name =  name
            profile_total.color = color
            profile_total.value = profile_data_th_total.iloc[:, 0]
            return (profile_total,)
        
class ProfileGeneratorCooling:
    def __init__(self, general_data_input:StandardBuildingProfileGeneralInput, cooling_data_input: StandardBuildingCoolingProfileInput): 
        self.simulation_year = general_data_input.simulation_year
        self.annual_demand = cooling_data_input.annual_demand
        self.temperature = general_data_input.temperature
        self.obj_cooling = CoolingProfileGenerator(self.simulation_year, self.annual_demand, self.temperature)
        self.sector = cooling_data_input.sector

    def generate_cooling_load_profile(self,) -> StandardLoadProfile:
        if self.sector == 'Residential':
            profile_data_cooling = self.obj_cooling.generate_load_profile_residential()
        if self.sector == 'Commercial':
            profile_data_cooling = self.obj_cooling.generate_load_profile_commercial()
        profile = StandardLoadProfile()
        profile.value =  profile_data_cooling.iloc[:, 0]
        profile.name = "Cooling demand"
        profile.color =  'blue'
        return profile

class ProfileGeneratorIndustrial:
    def __init__(self, general_data_input, electrical_data_input, thermal_data_input):
        dataframe = pd.DataFrame(index=pd.date_range(datetime.datetime(general_data_input.simulation_year, 1, 1, 0), periods=8760 * 4, freq="15T"))
        self.df_index = dataframe.index
        self.simulation_year = general_data_input.simulation_year
        self.annual_demand_elec= electrical_data_input.annual_demand
        self.annual_demand_thermal = thermal_data_input.annual_demand
        self.am = settime(general_data_input.begginig_workday)
        self.pm = settime(general_data_input.end_workday)
        self.week = [1, 2, 3, 4, 5]
        self.weekend = [0, 6, 7]
        self.profile_factors={
            "week": {"day":general_data_input.weekday_day_factor , "night": general_data_input.weekday_night_factor},
            "weekend": {"day": general_data_input.weekend_day_factor, "night": general_data_input.weekend_night_factor},
        }
        
    def generate_electrical_load_profile(self,):
        obj_el = IndustrialLoadProfile(self.df_index, holidays=holidays.Germany(years=self.simulation_year))
        profile_data_el = obj_el.simple_profile(self.annual_demand_elec, am=self.am, pm=self.pm, week=self.week, weekend=self.weekend, profile_factors=self.profile_factors)    
        profile_data_el = pd.DataFrame(profile_data_el)
        profile = StandardLoadProfile()
        profile.name = "Electrical demand"
        profile.color = ['#008000']
        profile.value = profile_data_el.iloc[:, 0]
        return profile 

    def generate_thermal_load_profile(self,):
        obj_th = IndustrialLoadProfile(self.df_index, holidays=holidays.Germany(years=self.simulation_year))
        profile_data_th = obj_th.simple_profile(self.annual_demand_thermal, am=self.am, pm=self.pm, week=self.week, weekend=self.weekend, profile_factors=self.profile_factors)
        profile_data_th.name = 'temperature_geo'
        profile_data_th = pd.DataFrame(profile_data_th)
        profile = StandardLoadProfile()
        profile.name = "Thermal demand"
        profile.color = ['#D53513']
        profile.value = profile_data_th.iloc[:, 0]
        return profile 



def map_subsector_to_demandlib() -> str:
    subsector_data = {
        StandardBuildingElectricityResidentialSubSector.Household: 'h0',
        StandardBuildingElectricityCommercialSubSector.Generaltrade_business_commercial:'g0',
        StandardBuildingElectricityCommercialSubSector.weekdays_Business:'g1',
        StandardBuildingElectricityCommercialSubSector.evening_Business:'g2',
        StandardBuildingElectricityCommercialSubSector.continuous_Business:'g3',
        StandardBuildingElectricityCommercialSubSector.shop_barber_shop:'g4',
        StandardBuildingElectricityCommercialSubSector.bakery:'g5',
        StandardBuildingElectricityCommercialSubSector.weekend_operation :'g6',
        StandardBuildingElectricityAgriculturalSubSector.general_farms:'l0',
        StandardBuildingElectricityAgriculturalSubSector.dairy_farms:'l1',
        StandardBuildingElectricityAgriculturalSubSector.other_farms:'l2',
        StandardBuildingHeatingResidentialSubSector.SingleFamilyHouse:'EFH',
        StandardBuildingHeatingResidentialSubSector.MultiFamilyHouse:'MFH',
        StandardBuildingHeatingCommercialSubSector.Metal_and_automotive:'GMK',
        StandardBuildingHeatingCommercialSubSector.Paper_and_printing:'GPD',
        StandardBuildingHeatingCommercialSubSector.Retail_and_wholesale:'GHA',
        StandardBuildingHeatingCommercialSubSector.Other_operational_services:'GBD',
        StandardBuildingHeatingCommercialSubSector.Local_authorities:'GKO',
        StandardBuildingHeatingCommercialSubSector.Accommodation:'GBH',
        StandardBuildingHeatingCommercialSubSector.Restaurants:'GGA',
        StandardBuildingHeatingCommercialSubSector.Bakery:'GBA',
        StandardBuildingHeatingCommercialSubSector.laundries_dry_cleaning:'GWA',
        StandardBuildingHeatingCommercialSubSector.Horticulture:'GGB',
        StandardBuildingHeatingCommercialSubSector.Household_like_business_enterprises:'GMF',
        StandardBuildingHeatingCommercialSubSector.Business_Commerce_Services: 'GHD',
    }

    return subsector_data


def map_wind_calss_to_demandlib() -> str:
    wind_class_data= {
        StandardBuildingHeatingWindClass.windy_area:0,
        StandardBuildingHeatingWindClass.Non_windy_area: 1,
    }
    return wind_class_data


def map_building_calss_to_demandlib() -> str:
    building_class_data= {
        StandardBuildingHeatingAgeClass.Old: 4,
        StandardBuildingHeatingAgeClass.Medium: 7,
        StandardBuildingHeatingAgeClass.New: 11,
    }
    return building_class_data

