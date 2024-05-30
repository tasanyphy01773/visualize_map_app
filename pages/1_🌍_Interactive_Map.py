import streamlit as st
import netCDF4 as nc
import numpy as np
import folium
import requests
import os

# Title of the app
st.title('Global U-Wind Visualization on Interactive Map')

# Function to download the data file
def download_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    else:
        return False

# Load wind data from netCDF file
@st.cache
def load_data(filepath):
    try:
        ds = nc.Dataset(filepath)
        u_wind = ds.variables['u_wind'][:]
        return u_wind, ds.variables['lat'][:], ds.variables['lon'][:]
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None, None, None

# URL of the .nc file and local filename
url = 'https://github.com/tasanyphy01773/visualize_map_app/releases/download/dataset/wind_global.nc'
filename = 'wind_global.nc'

# Download the file if it does not exist
if not os.path.exists(filename):
    result = download_file(url, filename)
    if not result:
        st.error('Failed to download file. Please check the URL or network settings.')

# Load the data
u_wind, lats, lons = load_data(filename)
if u_wind is not None:
    # Set up the folium map
    m = folium.Map(location=[0, 0], zoom_start=2)

    # Convert the U-wind data to a simple image that can be overlayed
    u_wind_img = np.flipud(u_wind[0])  # Flip to match the latitudes if necessary
    # Generate an image overlay
    bounds = [[lats.min(), lons.min()], [lats.max(), lons.max()]]
    folium.raster_layers.ImageOverlay(
        image=u_wind_img, bounds=bounds, colormap=lambda x: (x, x, 0.5, x)
    ).add_to(m)

    # Render in Streamlit
    folium_static(m)
else:
    st.error('Unable to load and plot data due to an error with the data files.')
