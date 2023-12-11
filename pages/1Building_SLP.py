import json

import pandas as pd
import streamlit as st

from streamlit_component.DataInput import (CoolingInput, ElectricalInput,
                                  GeneralDataInputBuilding, ThermalInput)
from src.moduel.ProfileRunner import (ProfileGeneratorCooling,
                                      ProfileGeneratorElectrical,
                                      ProfileGeneratorThermal)
from src.moduel.Visualizer import DataVisualizer
from src.moduel.Pydantic_validification import PydanticValidation

st.set_page_config(
page_title="mm.esd data explorer", layout = "wide") 
#region data input
st.title("Thermal-Electrical-Cooling Load Profile Generator")
general_data_input = GeneralDataInputBuilding()
general_data_input.run_general_data_input()
electrical_input = ElectricalInput()
electrical_input.run_electrical_input()
thermal_input = ThermalInput()
thermal_input.run_thermal_input()
cooling_input = CoolingInput()
cooling_input.run_cooling_input()


#export all of the json data
input_data_json = {
    "general_data":general_data_input.json(),
    "electrical_data":electrical_input.json(),
    "thermal_data":thermal_input.json(),
    "cooling_data":cooling_input.json(),

}
st.download_button(
    label="Download Json Input Data",
    data=json.dumps(input_data_json, indent=4),
    file_name="input_data.json",
    mime="application/json",
        )
# endregion

# region data validation Json
if st.checkbox("Upload your json file for input data"):
    with st.form("Upload your json file", clear_on_submit=True):
        uploaded_file = st.file_uploader("Upload your json file", type="json", accept_multiple_files=False)
        submit_button = st.form_submit_button("Submit")
        if submit_button and uploaded_file is not None:
            st.success("File uploaded successfully")
            input_data = json.load(uploaded_file)
            pydantic_validation = PydanticValidation()
            general_data_input = pydantic_validation.validation_general_data(input_data["general_data"])
            electrical_input = pydantic_validation.validation_electrical_data(input_data["electrical_data"])
            thermal_input = pydantic_validation.validation_thermal_data(input_data["thermal_data"])
            cooling_input = pydantic_validation.validation_cooling_data(input_data["cooling_data"])
            electrical_profile_obj = ProfileGeneratorElectrical(general_data_input,electrical_input)
            thermal_profile_obj = ProfileGeneratorThermal(general_data_input,thermal_input)
            cooling_profile_obj = ProfileGeneratorCooling(general_data_input,cooling_input)
        else:
            st.info("Please upload a json file")
else:
    electrical_profile_obj = ProfileGeneratorElectrical(general_data_input,electrical_input)
    thermal_profile_obj = ProfileGeneratorThermal(general_data_input,thermal_input)
    cooling_profile_obj = ProfileGeneratorCooling(general_data_input,cooling_input)
# endregion

# region gereate profile
electrical_profile = electrical_profile_obj.generate_electrical_load_profile()
thermal_profile = thermal_profile_obj.generate_thermal_load_profile()
cooling_profile = cooling_profile_obj.generate_cooling_load_profile()
# endregion


#region visualizer
tab_load_profile, tab_heat_map, tab_duration_curve = st.tabs(["Load profile","Heat map", "Duration curve"])
with tab_load_profile:
    st.write("Load profile")
    visualizer = DataVisualizer()
    visualizer.plot_load_profile(electrical_profile)
    visualizer.plot_load_profile(*thermal_profile)
    visualizer.plot_load_profile(cooling_profile)
    #download all the profiles
    all_profiles = {}
    all_profiles['Electrical Profile'] = electrical_profile.value
    if thermal_input.hwd_include:
        all_profiles['Total Thermal Profile'] = thermal_profile[0].value
        all_profiles['Domestic Hot Water Profile'] = thermal_profile[1].value
        all_profiles['Space Heating Profile'] = thermal_profile[2].value
    else:
        all_profiles['Total Thermal Profile'] = thermal_profile[0].value

    all_profiles['Cooling Profile'] = cooling_profile.value
    aligned_outside_temperature = general_data_input.temperature.reindex(all_profiles['Total Thermal Profile'].index).interpolate()
    all_profiles['Outside Temperature Profile'] = aligned_outside_temperature
    all_profiles_df = pd.concat(all_profiles.values(), axis=1, keys=all_profiles.keys())
    csv_data = all_profiles_df.to_csv().encode('utf-8')
    st.download_button(label='Download All Profile CSV Files', data=csv_data,
                    file_name='all_profiles.csv', mime='text/csv')

with tab_heat_map:
    st.write("Heat map")
    visualizer.plot_heatmap(electrical_profile, old_profile_name=electrical_input.subsector)
    visualizer.plot_heatmap(thermal_profile[0], old_profile_name='temperature_geo')
    visualizer.plot_heatmap(cooling_profile, old_profile_name='load_real')

with tab_duration_curve:
    st.write("Duration curve")
    visualizer.plot_duration_curve(electrical_profile, thermal_profile[0], cooling_profile)
#endregion


    





