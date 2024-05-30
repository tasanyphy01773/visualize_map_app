import streamlit as st
import rasterio
from rasterio.enums import Resampling
from leafmap.leafmap import netcdf_to_tif
import folium
from streamlit_folium import folium_static

st.title('Global U-Wind Visualization')

# Function to convert NetCDF to GeoTIFF
def convert_netcdf_to_geotiff(filename, tif_name):
    netcdf_to_tif(filename, tif_name, variables=["u_wind"], shift_lon=True)
    with rasterio.open(tif_name) as src:
        profile = src.profile
        profile.update({'crs': 'epsg:4326'})
        corrected_tif_path = 'wind_global_corrected.tif'
        with rasterio.open(corrected_tif_path, 'w', **profile) as dst:
            for i in range(1, src.count + 1):
                data = src.read(i, resampling=Resampling.nearest)
                dst.write(data, i)
    return corrected_tif_path

# Download and prepare data
filename = 'https://github.com/tasanyphy01773/visualize_map_app/releases/download/dataset/wind_global.nc'
tif_name = "wind_global.tif"
corrected_tif_path = convert_netcdf_to_geotiff(filename, tif_name)

if corrected_tif_path:
    # Create a Folium map
    m = folium.Map(location=[0, 0], zoom_start=2)
    folium.raster_layers.TileLayer(tiles=corrected_tif_path, attr='U-Wind').add_to(m)
    # Optionally add geojson for countries
    geojson_url = "https://github.com/opengeos/leafmap/raw/master/examples/data/countries.geojson"
    folium.GeoJson(geojson_url, name="Countries").add_to(m)
    folium.LayerControl().add_to(m)
    
    # Display map in Streamlit
    folium_static(m)
else:
    st.error("Failed to generate the map due to an error in the file conversion.")
