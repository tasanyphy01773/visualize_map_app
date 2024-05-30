import streamlit as st
import netCDF4 as nc
import numpy as np
import folium
import requests
import os
from PIL import Image
import io
import base64

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
    # Create a map
    m = folium.Map(location=[0, 0], zoom_start=2)

    # Normalize and scale the U-Wind data to convert to image
    scaled_wind = (255 * (u_wind[0] - np.min(u_wind[0])) / np.ptp(u_wind[0])).astype(np.uint8)
    image = Image.fromarray(scaled_wind, mode='L')
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    encoded_image = base64.b64encode(buffered.getvalue()).decode()

    # Generate the image overlay
    img_url = f"data:image/png;base64,{encoded_image}"
    bounds = [[lats.min(), lons.min()], [lats.max(), lons.max()]]
    folium.raster_layers.ImageOverlay(
        image=img_url, bounds=bounds, interactive=True, cross_origin=False
    ).add_to(m)

    # Display the map
    folium_static(m)
else:
    st.error('Unable to load and plot data due to an error with the data files.')
