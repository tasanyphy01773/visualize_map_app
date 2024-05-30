import streamlit as st
import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np

st.title('Global U-Wind Visualization')

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

file_path = 'https://raw.githubusercontent.com/tasanyphy01773/CLIM711_project/main/wind_global.nc'
data = load_data(file_path)
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
