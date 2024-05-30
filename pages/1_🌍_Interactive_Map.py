import streamlit as st
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import requests
import os
from io import BytesIO
import base64
import folium
from streamlit_folium import folium_static

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
        lats = ds.variables['lat'][:]
        lons = ds.variables['lon'][:]
        return u_wind, lats, lons
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None, None, None

url = 'https://github.com/tasanyphy01773/visualize_map_app/releases/download/dataset/wind_global.nc'
filename = 'wind_global.nc'

if not os.path.exists(filename):
    if not download_file(url, filename):
        st.error('Failed to download file. Please check the URL or network settings.')

u_wind, lats, lons = load_data(filename)
if u_wind is not None:
    if u_wind.ndim == 3:  # Assuming shape is [time, lat, lon]
        u_wind = u_wind[0, :, :]
    elif u_wind.ndim == 2:  # Assuming shape is [lat, lon]
        u_wind = u_wind[:, :]

    # Generate a plot
    fig, ax = plt.subplots()
    c = ax.imshow(u_wind, cmap='viridis')
    plt.axis('off')
    plt.colorbar(c)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    data = base64.b64encode(buf.getvalue()).decode()

    # Create a folium map
    m = folium.Map(location=[np.mean(lats), np.mean(lons)], zoom_start=2)
    folium.raster_layers.ImageOverlay(
        image=f"data:image/png;base64,{data}",
        bounds=[[lats.min(), lons.min()], [lats.max(), lons.max()]],
        interactive=True,
        cross_origin=False,
        zindex=1,
    ).add_to(m)
    folium.LayerControl().add_to(m)

    folium_static(m)
else:
    st.error('Unable to load and plot data due to an error with the data files.')
s