import pandas as pd
import streamlit as st
from pydantic import BaseModel, Field, ValidationError

import src.moduel.Streamlit_Runner as handler
from src.moduel.Data_Model import (StandardIndustrialProfileInput,
                                   StandardLoadProfile,
                                   StandardLoadProfilesResult)
from streamlit_component.DataInput import GeneralDataInputIndustrial
from src.moduel.Parameter import *
from src.moduel.Pydantic_validification import PydanticValidation

st.set_page_config(
        page_title="mm.esd data explorer", layout = "wide") 

#region data input
st.title("Thermal-Electrical-Cooling Load Profile Generator")
general_data_input = GeneralDataInputIndustrial()
general_data_input.run_data_input()
#endregion

#region pydantic validation
validification =PydanticValidation()
general_data_valid = validification.validation_general_industrial(general_data_input)
validification.json_industrial()
#endregion

#region generating profiles
obj_industrial = ProfileGeneratorIndustrial(general_data_valid, electrical_data_valid, thermal_data_valid)
profile_data_el = obj_industrial.generate_electrical_load_profile()
profile_data_th = obj_industrial.generate_thermal_load_profile()
# endregion


tab = handler.Tabs_industrial(obj_industrial)
tab.run_tabs()

visualized_profile_valid_elec = validification.validation_profile(tab.data_visualizer_el)
visualized_profile_valid_th = validification.validation_profile(tab.data_visualizer_th)

download_button_expander = st.expander("Download Output Data ")
with download_button_expander:
    tab.download_function()
#region duration curve

#endregion



