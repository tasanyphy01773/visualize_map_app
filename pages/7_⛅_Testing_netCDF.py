import streamlit as st
import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np
import requests
import os

st.title('Global U-Wind Visualization')

def download_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    else:
        return False

@st.cache
def load_data(filepath):
    try:
        ds = nc.Dataset(filepath)
        u_wind = ds.variables['u_wind'][:]
        v_wind = ds.variables['v_wind'][:]
        lats = ds.variables['lat'][:]
        lons = ds.variables['lon'][:]
        return u_wind, v_wind, lats, lons
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None, None, None, None

# URL of the .nc file
url = 'https://github.com/tasanyphy01773/visualize_map_app/releases/download/dataset/wind_global.nc'
filename = 'wind_global.nc'

# Check if file is not already downloaded
if not os.path.exists(filename):
    result = download_file(url, filename)
    if not result:
        st.error('Failed to download file. Please check the URL or network settings.')

data = load_data(filename)
if data[0] is not None:
    u_wind, v_wind, lats, lons = data
    lon, lat = np.meshgrid(lons, lats)

    if st.checkbox('Show U-Wind Map'):
        fig, ax = plt.subplots()
        c = ax.pcolormesh(lon, lat, u_wind, shading='auto')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_title('Global U-Wind')
        plt.colorbar(c, ax=ax, label='U-Wind (units)')
        st.pyplot(fig)

    if st.checkbox('Show V-Wind Map'):
        fig, ax = plt.subplots()
        c = ax.pcolormesh(lon, lat, v_wind, shading='auto')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_title('Global V-Wind')
        plt.colorbar(c, ax=ax, label='V-Wind (units)')
        st.pyplot(fig)
else:
    st.error('Unable to load and plot data due to an error with the data files.')
