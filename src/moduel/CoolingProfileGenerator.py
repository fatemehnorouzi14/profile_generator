import datetime
import math
import os

import holidays
import pandas as pd


class CoolingProfileGenerator:
    def __init__(self,simulation_year,annual_demand):
        self.simulation_year = simulation_year
        self.annual_demand = annual_demand
        self.generic_profile_residential = pd.read_csv(datapath_generic_profile_residential)
        self.generic_profile_commercial = pd.read_csv(datapath_generic_profile_commercial)
        self.temperature = pd.read_csv(datapath_temperature)
        self.holidays = holidays.Germany()
        self.holidays._populate(self.simulation_year)
        self.df = pd.DataFrame(index=pd.date_range(datetime.datetime(self.simulation_year, 1, 1, 0), periods=8760, freq="H"))
    

    def generate_load_profile_residential(self):
        generic_profile_residential = self.generic_profile_residential[self.generic_profile_residential['NUTS2_code'] == 'AT11']
        generic_profile_residential = generic_profile_residential.drop(columns=['season', 'process'])
        start_date = datetime.datetime(self.simulation_year, 1, 1)
        end_date  = start_date + datetime.timedelta(days=364, hours=23)
        timestamps = pd.date_range(start=start_date, end=end_date, freq='H')
        df = pd.DataFrame({'Timestamp': timestamps})
        df["temperature"] = self.temperature["temperature"].apply(math.ceil)

        df['day_type'] = df['Timestamp'].apply(lambda x: self.calculate_day_type(x, self.holidays))
        df['NUTS2_code'] = 'AT11'
        df['hour'] = df['Timestamp'].dt.hour

        merged_df = pd.merge(df, generic_profile_residential, on=['temperature', 'day_type', 'hour'], how='left')
        merged_df.rename(columns={'load': 'load_column'}, inplace=True)
        merged_df['load_column'].fillna(0.0, inplace=True)

        # Calculate the total sum of the generic yearlong profile and divide the desired annual demand by it
        total_sum = merged_df['load_column'].sum()
        scale_factor = self.annual_demand / total_sum
        merged_df['load_real'] = merged_df['load_column'] * scale_factor
        df = merged_df[['Timestamp', 'load_real']]
        df = pd.Series(df['load_real'].values,name='load_real', index=self.df.index)
        df = pd.DataFrame(df)

        return df
    
    def generate_load_profile_commercial(self):
        generic_profile_commercial = self.generic_profile_commercial[self.generic_profile_commercial['NUTS2_code'] == 'AT11']
        generic_profile_commercial = generic_profile_commercial.drop(columns=['season', 'process'])
        start_date = datetime.datetime(self.simulation_year, 1, 1)
        end_date = start_date + datetime.timedelta(days=364, hours=23)
        timestamps = pd.date_range(start=start_date, end=end_date, freq='H')
        df = pd.DataFrame({'Timestamp': timestamps})
        df["temperature"] = self.temperature["temperature"].apply(math.ceil)

        df['day_type'] = df['Timestamp'].apply(lambda x: self.calculate_day_type(x, self.holidays))
        df['NUTS2_code'] = 'AT11'
        df['hour'] = df['Timestamp'].dt.hour

        merged_df = pd.merge(df, generic_profile_commercial, on=['temperature', 'day_type', 'hour'], how='left')
        merged_df.rename(columns={'load': 'load_column'}, inplace=True)
        merged_df['load_column'].fillna(0.0, inplace=True)

        # Calculate the total sum of the generic yearlong profile and divide the desired annual demand by it
        total_sum = merged_df['load_column'].sum()
        scale_factor = self.annual_demand / total_sum
        merged_df['load_real'] = merged_df['load_column'] * scale_factor
        df = merged_df[['Timestamp', 'load_real']]
        df = pd.Series(df['load_real'].values,name='load_real', index=self.df.index)
        df = pd.DataFrame(df)
    
        return df

    @staticmethod
    def calculate_day_type(timestamp, holidays):
        if timestamp.weekday() in [5, 6] or timestamp.date() in holidays:
            # weekend and holiday
            return 1
        elif timestamp.weekday() == 0:
            # Monday, start of week
            return 2
        else:
            # weekdays
            return 0
        


filename_temperature = "temperature.csv"
dirname = os.getcwd()
datapath_temperature = os.path.join(dirname,'src', "resources", filename_temperature)
filename_generic_profile_residential = "generic_profile_residential.csv"
datapath_generic_profile_residential = os.path.join(dirname,'src', "resources", filename_generic_profile_residential)
filename_generic_profile_commercial = "generic_profile_tertiary.csv"
datapath_generic_profile_commercial = os.path.join(dirname,'src', "resources", filename_generic_profile_commercial)







