import streamlit as st
import leafmap.foliumap as leafmap
import os
import requests

# Title of the app
st.title('Global U-Wind Visualization')

# Function to download the NetCDF file if not present
def download_file(url, filename):
    r = requests.get(url, allow_redirects=True)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(r.content)

# URL and filename of the NetCDF file
netcdf_url = 'https://github.com/tasanyphy01773/visualize_map_app/releases/download/dataset/wind_global.nc'
netcdf_filename = 'wind_global.nc'

# Download the file if it does not exist locally
if not os.path.exists(netcdf_filename):
    download_file(netcdf_url, netcdf_filename)

# Initialize a map
m = leafmap.Map(center=(0, 0), zoom=2, layers_control=True)

# Add the u_wind layer from the NetCDF file
m.add_netcdf(
    netcdf_filename,
    variables=["u_wind"],
    palette="coolwarm",
    shift_lon=False,
    layer_name="U-Wind",
    indexes=[0],  # Assuming time dimension is first and only one time step is needed
    x_dim='lon',  # The longitude dimension based on your NetCDF details
    y_dim='lat'   # The latitude dimension based on your NetCDF details
)

# Display the map in the Streamlit app
m.to_streamlit(height=700)
