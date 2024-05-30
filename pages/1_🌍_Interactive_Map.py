
import streamlit as st
import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np
import requests
import os
import leafmap.foliumap as leafmap
import rasterio
from rasterio.enums import Resampling

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

def convert_netcdf_to_geotiff(filename, tif_name, variable):
    ds = nc.Dataset(filename)
    data = ds.variables[variable][:]
    lats = ds.variables['lat'][:]
    lons = ds.variables['lon'][:]
    transform = rasterio.transform.from_bounds(lons.min(), lats.min(), lons.max(), lats.max(), data.shape[2], data.shape[1])

    with rasterio.open(tif_name, 'w', driver='GTiff', height=data.shape[1], width=data.shape[2],
                       count=1, dtype=data.dtype, crs='EPSG:4326', transform=transform) as dst:
        dst.write(data[0, :, :], 1)  # Adjust this index based on your data
    return tif_name

# URL of the .nc file
url = 'https://github.com/tasanyphy01773/visualize_map_app/releases/download/dataset/wind_global.nc'
filename = 'wind_global.nc'

# Check if file is not already downloaded
if not os.path.exists(filename):
    result = download_file(url, filename)
    if not result:
        st.error('Failed to download file. Please check the URL or network settings.')

# Convert NetCDF to GeoTIFF
tif_name = 'wind_global_u_wind.tif'
corrected_tif_path = convert_netcdf_to_geotiff(filename, tif_name, 'u_wind')

# Display map
markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("Interactive Map")

col1, col2 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("OpenTopoMap")

with col2:
    basemap = st.selectbox("Select a basemap:", options, index)

with col1:
    m = leafmap.Map(
        locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
    )
    m.add_raster(corrected_tif_path, palette="coolwarm", layer_name="u_wind")
    m.add_basemap(basemap)
    m.to_streamlit(height=700)







# import streamlit as st
# import netCDF4 as nc
# import matplotlib.pyplot as plt
# import numpy as np
# import requests
# import os

# st.title('Global U-Wind Visualization')

# def download_file(url, filename):
#     response = requests.get(url)
#     if response.status_code == 200:
#         with open(filename, 'wb') as f:
#             f.write(response.content)
#         return True
#     else:
#         return False

# @st.cache
# def load_data(filepath):
#     try:
#         ds = nc.Dataset(filepath)
#         u_wind = ds.variables['u_wind'][:]
#         v_wind = ds.variables['v_wind'][:]
#         lats = ds.variables['lat'][:]
#         lons = ds.variables['lon'][:]
#         return u_wind, v_wind, lats, lons
#     except Exception as e:
#         st.error(f"Failed to load data: {e}")
#         return None, None, None, None

# # URL of the .nc file
# url = 'https://github.com/tasanyphy01773/visualize_map_app/releases/download/dataset/wind_global.nc'
# filename = 'wind_global.nc'

# # Check if file is not already downloaded
# if not os.path.exists(filename):
#     result = download_file(url, filename)
#     if not result:
#         st.error('Failed to download file. Please check the URL or network settings.')

# # data = load_data(filename)

# import leafmap.foliumap as leafmap

# markdown = """
# A Streamlit map template
# <https://github.com/opengeos/streamlit-map-template>
# """

# st.sidebar.title("About")
# st.sidebar.info(markdown)
# logo = "https://i.imgur.com/UbOXYAU.png"
# st.sidebar.image(logo)


# st.title("Interactive Map")

# col1, col2 = st.columns([4, 1])
# options = list(leafmap.basemaps.keys())
# index = options.index("OpenTopoMap")

# with col2:

#     basemap = st.selectbox("Select a basemap:", options, index)


# with col1:

#     m = leafmap.Map(
#         locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
#     )
#     m.add_netcdf(
#         filename,
#         variables=["u_wind"],
#         palette="coolwarm",
#         shift_lon=True,
#         layer_name="u_wind",
#         indexes=[1]  # Ensure that this index is applicable for your data
#     )

#     m.add_basemap(basemap)
#     m.to_streamlit(height=700)
