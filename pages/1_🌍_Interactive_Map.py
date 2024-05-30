
import streamlit as st
import leafmap.foliumap as leafmap
import netCDF4 as nc
import numpy as np
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
        v_wind = ds.variables['v_wind'][:]
        lats = ds.variables['lat'][:]
        lons = ds.variables['lon'][:]
        return u_wind, v_wind, lats, lons
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None, None, None, None

# URL of the .nc file and local filename
url = 'https://github.com/tasanyphy01773/visualize_map_app/releases/download/dataset/wind_global.nc'
filename = 'wind_global.nc'

# Download the file if it does not exist
if not os.path.exists(filename):
    result = download_file(url, filename)
    if not result:
        st.error('Failed to download file. Please check the URL or network settings.')

# Load the data
data = load_data(filename)
if data[0] is not None:
    u_wind, v_wind, lats, lons = data

    col1, col2 = st.columns([4, 1])
    options = list(leafmap.basemaps.keys())
    index = options.index("OpenTopoMap")

    with col2:
        basemap = st.selectbox("Select a basemap:", options, index)

    with col1:
        m = leafmap.Map(locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
        m.add_basemap(basemap)

        # Add wind vectors as arrows
        for i in range(0, len(lats), 10):  # Skipping steps for performance
            for j in range(0, len(lons), 10):
                lat = lats[i]
                lon = lons[j]
                u = u_wind[0, i, j]  # Assuming time dimension is first
                v = v_wind[0, i, j]
                magnitude = np.sqrt(u**2 + v**2)
                angle = np.arctan2(v, u) * 180 / np.pi  # Convert to degrees
                # Create an arrow (need to implement or find a plugin that supports it)
                # Placeholder for actual arrow drawing, as leafmap does not support it directly
                # Implement or use plugins like folium.plugins.BeautifyIcon if available
                m.add_marker(location=(lat, lon), popup=f"Wind Speed: {magnitude:.2f}, Direction: {angle:.2f}°")

        m.to_streamlit(height=700)
else:
    st.error('Unable to load and plot data due to an error with the data files.')




# import streamlit as st
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
#     m.add_basemap(basemap)
#     m.to_streamlit(height=700)
