from datetime import time
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

# region General Data Input
st.subheader('General Data Input')
start_year, start_month, start_day, resolution = st.columns(4)

with start_year:
    start_year_val = st.number_input("Start year:", 2000, 2100, 2023, key="unique_key_value20")
with start_month:
    start_month_val = st.number_input("Start month:", 1, 12, 1, key="unique_key_value11")
with start_day:
    start_day_val = st.number_input("Start day:", 1, 31, 1, key="unique_key_value22")
with resolution:
    options = ['60min', '45 min', '30 min', '15min', '05min']
    resolution_val = st.selectbox('Resolution:', options, key="resolution_key")
    resolution_int = int(resolution_val[:2])

# Save entered data
general_data = {
    'Start Year': start_year_val,
    'Start Month': start_month_val,
    'Start Day': start_day_val,
    'Resolution': resolution_val,
}

st.subheader('Station Data Input')
number_stations = st.container()

with number_stations:
    station_num = int(st.number_input("Enter the number of stations:", min_value=1, value=1, step=1, max_value=6))

stations = []

for i in range(station_num):
    name_station, num_charger, charger_data = st.columns(3)

    with name_station:
        station_name = st.text_input(f"Station {i + 1} Name:", value=f"Station {i + 1}", key=f'station_name_{i}')
    with num_charger:
        charger_number = st.number_input(f"Charger No.:", min_value=1, value=1, step=1, key=f'charging_station_number_{i}')
    charger_data_list = []

    for j in range(charger_number):
        name_charger, day_week, arrive_time, stay_l = st.columns(4)

        with name_charger:
            charger_name = st.text_input(f"Charger {j + 1} Name:", value=f"Charger {j + 1}", key=f'charging_station_name_{i}_{j}')
        with day_week:
            options_week_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_of_week = st.multiselect(f'week day(s):', options_week_day, default=['Sunday'],
                                         key=f'day_of_week_{i}_{j}')

        with arrive_time:
            time_arrival = st.time_input(label="Arrival time", value=time(0, 0), key=f'arrival_time_{i}_{j}',
                                         step=resolution_int * 60)
        with stay_l:
            length_of_stay = st.time_input(label="Length of Stay ", value=time(1, 0), key=f'length_time_{i}_{j}',
                                           step=resolution_int * 60)

        charger_data_list.append({
            'Charger Station Name': charger_name,
            'Day(s) of Week': day_of_week,
            'Arrival Time': time_arrival,
            "Stay Length (h)": length_of_stay,
        })

    stations.append({
        'name_station': station_name,
        'num_charger': charger_number,
        'charger station data': charger_data_list
    })
# endregion
@st.cache_data(hash_funcs={pd.DataFrame: lambda x: None})
def process_data(general_data, stations):
    df_index = pd.date_range(
        start=f'{general_data["Start Year"]}-{general_data["Start Month"]:02d}-{general_data["Start Day"]:02d}',
        end=f'{general_data["Start Year"]}-12-31 23:59:00', freq=general_data["Resolution"])
    df = pd.DataFrame(index=df_index)
    df['weekday'] = df.index.day_name()
    df['resolution'] = resolution_int
    df.index.name = 'Timestamp'

    for station in stations:
        station_name = station["name_station"]

        for charger_station in station["charger station data"]:
            charger_name = charger_station["Charger Station Name"]
            week_day = charger_station["Day(s) of Week"]
            arrival_time = charger_station["Arrival Time"]
            stay_length = charger_station["Stay Length (h)"]

            soc_column_name = f"SOC_{station_name}_{charger_name}"
            df[soc_column_name] = -2  # Initialize with -2

            discharge_column_name = f"DISCHARGE_{station_name}_{charger_name}"
            df[discharge_column_name] = 1  # Initialize with 1, assuming it's the default state

            for day in week_day:
                matching_days = df.index[df.index.day_name() == day]

                for specific_day in matching_days:
                    arrival_datetime = specific_day.normalize() + pd.Timedelta(hours=arrival_time.hour,
                                                                                minutes=arrival_time.minute)
                    end_datetime = arrival_datetime + pd.Timedelta(hours=stay_length.hour, minutes=stay_length.minute)

                    if end_datetime > df.index[-1]:
                        df.loc[arrival_datetime, soc_column_name] = 0
                        df.loc[(df.index >= arrival_datetime) & (df.index <= df.index[-1]), discharge_column_name] = 0
                    else:
                        df.loc[arrival_datetime, soc_column_name] = 0
                        df.loc[end_datetime, soc_column_name] = 1
                        df.loc[(df.index >= arrival_datetime) & (df.index < end_datetime),
                               discharge_column_name] = 0
    return df

# Main button to process data
if st.button('Process'):
    df = process_data(general_data, stations)
    st.write(df)

    # region Display Data
    csv_file = df.to_csv(index=True, sep=';')
    st.download_button(label="Download CSV", data=csv_file, file_name='load_profile_Emobility.csv', mime='text/csv')
    # endregion
