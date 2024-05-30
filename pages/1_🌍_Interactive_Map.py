import streamlit as st
import leafmap.foliumap as leafmap
import os
import requests

def download_file(url, filename):
    """ Helper function to download a file """
    r = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(r.content)

# Title of the app
st.title('Global Wind Visualization')

# URL of the .nc file
netcdf_url = 'https://github.com/tasanyphy01773/visualize_map_app/releases/download/dataset/wind_global.nc'
netcdf_filename = 'wind_global.nc'

# Download the file if it does not exist
if not os.path.exists(netcdf_filename):
    download_file(netcdf_url, netcdf_filename)

# Initialize the map
m = leafmap.Map(layers_control=True)

# Add each variable as a separate layer
variables = ["v_wind", "u_wind"]
for var in variables:
    m.add_netcdf(
        netcdf_filename,
        variables=[var],
        palette="coolwarm",
        shift_lon=True,
        layer_name=var,
        indexes=[0]  # Adjust this index according to your data dimensions
    )

# Add GeoJSON for countries (assuming you have a valid GeoJSON file or URL)
geojson_url = 'https://your_geojson_url_here'  # Update with your GeoJSON file URL if applicable
m.add_geojson(geojson_url, layer_name="Countries")

# Display the map in Streamlit
folium_static(m)
