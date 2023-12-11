from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseConfig, BaseModel, Field

# Define Pydantic Models

class StandardBuildingProfileGeneralInput(BaseModel):
    simulation_year: int = Field(2023, ge=1900, le=2100, description='Base year for simulation')
    #temperature: Any
    #country: str = "DE"  # todo long term:Implement default values from holidays library


class StandardBuildingElectricitySector(str, Enum):
    Residential = "Residential"
    Commercial = "Commercial"
    Agricultural = "Agricultural"

class StandardBuildingElectricityResidentialSubSector(str, Enum):
    Household = "Household"

class StandardBuildingElectricityCommercialSubSector(str, Enum):
    Generaltrade_business_commercial = "General trade/business/commercial"
    weekdays_Business = 'Business on weekdays 8 a.m. - 6 p.m.'
    evening_Business = 'Businesses with heavy to predominant consumption in the evening hours'
    continuous_Business = 'Continuous business'
    shop_barber_shop = 'Shop/barber shop'
    bakery = 'Bakery'
    weekend_operation = 'Weekend operation'
    
class StandardBuildingElectricityAgriculturalSubSector(str, Enum):
    general_farms = 'General farms'
    dairy_farms = 'Farms with dairy farming/part-time animal husbandry'
    other_farms = 'Other farms'

class StandardBuildingElectricityIndustrialSubSector(str, Enum):
    Industrial = 'Industrial'


class StandardBuildingElectricityProfileInput(BaseModel):
    sector: StandardBuildingElectricitySector
    subsector_name: Union[StandardBuildingElectricityResidentialSubSector, 
                    StandardBuildingElectricityCommercialSubSector,
                    StandardBuildingElectricityAgriculturalSubSector,
                    StandardBuildingElectricityIndustrialSubSector]
    subsector: Optional[str] = Field(None, description='My optional string field')
    annual_demand: float = Field(80, ge=0, description='Annual demand in MWh')
    

class StandardBuildingHeatingSector(str, Enum):
    Residential = "Residential"
    Commercial = "Commercial"

class StandardBuildingHeatingResidentialSubSector(str, Enum):
    SingleFamilyHouse = "Single-family house"
    MultiFamilyHouse = 'Multi-family house'

class StandardBuildingHeatingCommercialSubSector(str, Enum):
    Metal_and_automotive = 'Metal and automotive'
    Paper_and_printing = 'Paper and printing'
    Retail_and_wholesale = 'Retail and wholesale'
    Other_operational_services = 'Other operational services'
    Local_authorities = 'Local authorities, credit institutions and insurance companies'
    Accommodation = 'Accommodation'
    Restaurants = 'Restaurants'
    Bakery = 'Bakery'
    laundries_dry_cleaning = 'laundries, dry cleaning'
    Horticulture = 'Horticulture'
    Household_like_business_enterprises = 'Household-like business enterprises'
    Business_Commerce_Services = 'Total load profile Business/Commerce/Services'

class StandardBuildingHeatingIndustrialSubSector(str, Enum):
    Industrial = 'Industrial'

class StandardBuildingHeatingWindClass(str, Enum):
    windy_area = 'Windy area'
    Non_windy_area= 'Non windy area'

class StandardBuildingHeatingAgeClass(str, Enum):
    Old = 'Before_1973'
    Medium = 'Between_1973_1989'
    New = 'After_1990'


class StandardBuildingHeatingProfileInput(BaseModel):
    sector: StandardBuildingHeatingSector
    subsector_name: Union[StandardBuildingHeatingResidentialSubSector,
                          StandardBuildingHeatingCommercialSubSector,
                          StandardBuildingHeatingIndustrialSubSector]
    subsector: Optional[str] = Field(None, description='My optional string field')
    wind_class: Optional[bool] = Field(None, description='My optional boolean field')
    wind_class_name: Optional[str] = Field(None, description='My optional string field')
    building_class: Optional[int] = Field(None, ge=0, description='Building class, an integer greater than or equal to 0')
    building_class_name: Optional[str] = Field(None, description='My optional string field')
    annual_demand: Optional[float] = Field(None, ge=0, description='Optional annual demand in MWh greater than or equal to 0')
    hwd_include: Optional[bool] = Field(None, description='My optional boolean field')
    slp: Optional[bool] = Field(None, description='My optional boolean field')
    dict_days: Optional[Dict[str, float]] = None


class StandardBuildingCoolingSector(str, Enum):
    Residential = "Residential"
    Commercial = "Commercial"

class StandardBuildingCoolingProfileInput(BaseModel):
    sector: StandardBuildingCoolingSector
    annual_demand: float = Field(80, ge=0, description='Annual demand in MWh')

class StandardBuildingProfileInputs(BaseModel):
    generalInfo: StandardBuildingProfileGeneralInput
    electricity: StandardBuildingElectricityProfileInput
    heating: StandardBuildingHeatingProfileInput
    cooling: StandardBuildingCoolingProfileInput

class StandardIndustrialProfileInput(StandardBuildingProfileGeneralInput):
    simulation_year: int = Field(2023, ge=1900, le=2100, description='Base year for simulation')
    begginig_workday: int = Field(8, ge=0, le=24, description='Beginning of workday in hours')
    end_workday:int = Field(16, ge=0, le=24, description='End of workday in hours')
    weekday_day_factor: float = Field(1.0, ge=0, le=1)
    weekday_night_factor: float = Field(0.8, ge=0, le=1)
    weekend_day_factor: float = Field(0.0, ge=0, le=1)
    weekend_night_factor: float = Field(0.0, ge=0, le=1)
    annual_demand_el: float = Field(80, ge=0, description='Annual electrical demand in MWh')
    annual_demand_th: float = Field(80, ge=0, description='Annual thermal demand in MWh')

class StandardLoadProfile(BaseModel):                         
    value: List[float] = None
    name: Optional[str] = Field(None, description='list of profile names')
    color: Optional[str] = Field(None, description='list of profile colors')
    class Config(BaseConfig):
        arbitrary_types_allowed = True

    def get_min(self):
        return f'{min(self.value):.2f}' if self.value is not None else None

    def get_average(self):
        return f'{sum(self.value)/len(self.value):.2f}' if self.value is not None else None

    def get_sum(self, name_sector):
        if name_sector == "Electrical demand":
            subdivider = 4000
        else:
            subdivider = 1000
        return f'{sum(self.value)/subdivider:.2f}' if self.value is not None else None

    def get_max(self):
        return f'{max(self.value):.2f}' if self.value is not None else None

    def getDateAxis(self, simulation_year):
        # todo: Implement DateTimeAxisGenerationFromYearAndLengthOfValues
        pass

class StandardLoadProfilesResult(BaseModel):
    profiles: list[StandardLoadProfile]
