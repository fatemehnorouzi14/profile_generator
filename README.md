

# Profile Generator Application

## About

The Profile Generator is a software tool that offers a variety of load profiles for different sectors. The available profiles include:

1. **Residential Sector:**
   - Electrical Load Profiles
   - Thermal Load Profiles
   - Cooling Load Profiles

2. **Commercial Sector:**
   - Electrical Load Profiles
   - Thermal Load Profiles
   - Cooling Load Profiles

3. **Industrial Sector:**
   - Electrical Load Profiles
   - Thermal Load Profiles

Users can access and generate the respective electrical, thermal, and cooling load profiles based on their input data. These profiles provide insights into the energy consumption and demand patterns specific to each sector, enabling better analysis and planning.

## Features

- Generate Electrical, Thermal, and Cooling Load Profiles for Residential, Commercial, and Industrial Sectors.
- Visualize profiles in different tabs, including time series view, heat map, and duration curve graph.
- Option to upload profile data in CSV format.

## Dependencies

This application relies on the following libraries:

- `Python`
- `streamlit`
- `pandas`
- `plotly`
- `numpy`
- `holidays`
- `datetime`
- `plotly.graph_objects`



## Usage

To generate load profiles, follow these steps:

1. Install the required dependencies as mentioned above.
2. Run the application using the following command:

   ```bash
   streamlit run app.py
   ```

3. The application will open in your browser.
4. Provide input parameters for electrical, heating, and cooling energy demands.
5. The application will display load profiles, heat maps, and duration curves for the generated profiles indifferent tabs.
6. You can download the generated load profiles as CSV files using the provided download buttons.

## Data Sources

- [BDEW Model for Electrical and Heating Load Profiles](https://mediatum.ub.tum.de/doc/601557/601557.pdf)
- [Cooling Load Profile Model (Hotmaps Project)](https://www.hotmaps-project.eu/wp-content/uploads/2018/03/D2.3-Hotmaps_for-upload_revised-final_.pdf)

For more information about the demandlib library, refer to the [documentation](https://demandlib.readthedocs.io/en/latest/).

## License
