import streamlit as st
import netCDF4 as nc
import numpy as np
import requests
import os
import folium
from streamlit_folium import folium_static

st.title('Global U-Wind Visualization')

# Function to download the NetCDF file
def download_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    else:
        return False

# Function to load data from NetCDF file
@st.cache(allow_output_mutation=True)
def load_data(filepath):
    try:
        ds = nc.Dataset(filepath)
        u_wind = ds.variables['u_wind'][:]
        lats = ds.variables['lat'][:]
        lons = ds.variables['lon'][:]
        return u_wind, lats, lons
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None, None, None

# Download URL and filename for the NetCDF file
url = 'https://github.com/tasanyphy01773/visualize_map_app/releases/download/dataset/wind_global.nc'
filename = 'wind_global.nc'

# Download the file if it doesn't exist
if not os.path.exists(filename):
    result = download_file(url, filename)
    if not result:
        st.error('Failed to download file. Please check the URL or network settings.')

# Load data
u_wind, lats, lons = load_data(filename)
if u_wind is not None:
    # Check if there's a time dimension and select the first timestep if present
    if u_wind.ndim == 3:  # Assuming shape is [time, lat, lon]
        u_wind = u_wind[0, :, :]
    elif u_wind.ndim == 2:  # Assuming shape is [lat, lon]
        u_wind = u_wind[:, :]

    # Meshgrid for longitude and latitude
    lon, lat = np.meshgrid(lons, lats)
    
    # Creating a Folium map
    m = folium.Map(location=[0, 0], zoom_start=2)
    
    # Add U-Wind data to map
    folium.raster_layers.ImageOverlay(
        image=u_wind,
        bounds=[[lat.min(), lon.min()], [lat.max(), lon.max()]],
        colormap=lambda x: (1.0, 1.0, 1.0, x/np.nanmax(u_wind)),  # Normalize the opacity
        name='U-Wind',
    ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Show map in Streamlit
    folium_static(m)

else:
    st.error('Unable to load and plot data due to an error with the data files.')
