"""
# Frontpage of mmesd data explorer
"""
import warnings

warnings.filterwarnings("default")

import streamlit as st

st.set_page_config(
    page_title="mm.esd data explorer", layout = "wide")

import src.moduel.DataFileImporter as importer

soft_ware_about = st.expander("About the software")
with soft_ware_about:
    st.markdown("This software offers a variety of load profiles for different sectors. The available profiles include:")
    st.markdown("1. Building SLP:")
    st.markdown("   - Electrical Load Profiles")
    st.markdown("   - Thermal Load Profiles")
    st.markdown("   - Cooling Load Profiles")
    st.markdown("2. Industrial SLP:")
    st.markdown("   - Electrical Load Profiles")
    st.markdown("   - Thermal Load Profiles")
    st.markdown("For each sector, users can access and generate the respective electrical, thermal, and cooling load profiles based on their input data. These profiles provide insights into the energy consumption and demand patterns specific to each sector, enabling better analysis and planning.")
    st.markdown("Once the data is entered, the application generates and visualizes the profiles in different tabs. The first tab presents a time series view, allowing users to explore the profiles over time. The second tab displays a heat map, providing a graphical representation of the load patterns. The third tab showcases a duration curve graph, illustrating the distribution of load intensities.")
    st.markdown("The residential and commercial sectors' profiles are accessible through the Building SLP page, while the industrial sector's profiles can be found on the Industrial SLP page. Furthermore, users have the option to download the profile data in CSV format and the entered input data in Json format at the bottom of the page.")
    st.markdown("This application relies on demandlib library which is based on the BDEW model for electrical and heating load profiles and incorporates the cooling load profile model developed by the Hotmaps project.")
    st.markdown("For more information about the BDEW model used to generate the electrical and heating load profiles click [here](https://mediatum.ub.tum.de/doc/601557/601557.pdf)")
    st.markdown("For more information about the model used to generate the cooling load profile click [here](https://www.hotmaps-project.eu/wp-content/uploads/2018/03/D2.3-Hotmaps_for-upload_revised-final_.pdf)")
    st.markdown("Information about demandlib library can be found [here](https://demandlib.readthedocs.io/en/latest/)")
image = importer.readImage("MotivationPicture.png")

st.image(image)
st.sidebar.title("About")
st.sidebar.info(
    """
    Our team provides algorithms, data and visualization for infrastructure design of decentralized energy systems.
    """
)


