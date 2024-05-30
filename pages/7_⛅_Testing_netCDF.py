import streamlit as st
import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np

# Title of the app
st.title('Global U-Wind Visualization New')

# Loading netCDF data
@st.cache  # This decorator helps cache the data to speed up app reloads
def load_data(filepath):
    ds = nc.Dataset(filepath)
    u_wind = ds.variables['u_wind'][:]
    v_wind = ds.variables['v_wind'][:]
    lats = ds.variables['lat'][:]  # Adjust variable names as necessary
    lons = ds.variables['lon'][:]
    return u_wind, v_wind, lats, lons

# File path to your netCDF file
file_path = 'https://raw.githubusercontent.com/tasanyphy01773/CLIM711_project/main/wind_global.nc' # I had to upload it in different folder
u_wind, v_wind, lats, lons = load_data(file_path)

# Create a meshgrid for plotting
lon, lat = np.meshgrid(lons, lats)

# Streamlit widget to toggle visibility
if st.checkbox('Show U-Wind Map'):
    fig, ax = plt.subplots()
    c = ax.pcolormesh(lon, lat, u_wind, shading='auto')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Global U-Wind')
    plt.colorbar(c, ax=ax, label='U-Wind (units)')
    st.pyplot(fig)


# Streamlit widget to toggle visibility
if st.checkbox('Show V-Wind Map'):
    fig, ax = plt.subplots()
    c = ax.pcolormesh(lon, lat, v_wind, shading='auto')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Global V-Wind')
    plt.colorbar(c, ax=ax, label='V-Wind (units)')
    st.pyplot(fig)