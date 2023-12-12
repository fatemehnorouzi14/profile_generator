import json

import pandas as pd
import streamlit as st

from streamlit_component.DataInput import (CoolingInput, ElectricalInput,
                                  GeneralDataInputBuilding, ThermalInput, streamlit_visulization, pydantic)
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
        input_data = None
        if submit_button and uploaded_file is not None:
            st.success("File uploaded successfully")
            input_data = json.load(uploaded_file)
        else:
            st.error("Please upload a json file")
    with st.container():
        if input_data is not None:
            general_data_input_valid, electrical_input_valid, thermal_input_valid, cooling_input_valid = pydantic(input_data, general_data_input)
            streamlit_visulization(general_data_input_valid,electrical_input_valid,thermal_input_valid,cooling_input_valid)
else:
    streamlit_visulization(general_data_input,electrical_input,thermal_input,cooling_input)
# endregion 