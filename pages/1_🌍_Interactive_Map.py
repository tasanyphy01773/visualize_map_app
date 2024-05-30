import streamlit as st
import rasterio
from rasterio.enums import Resampling
from leafmap.leafmap import netcdf_to_tif, Map

# Function to convert NetCDF to GeoTIFF
def convert_netcdf_to_geotiff(filename, tif_name):
    netcdf_to_tif(filename, tif_name, variables=["u_wind", "v_wind"], shift_lon=True)
    with rasterio.open(tif_name) as src:
        profile = src.profile
        profile.update({'crs': 'epsg:4326'})
        corrected_tif_path = 'wind_global_corrected.tif'
        with rasterio.open(corrected_tif_path, 'w', **profile) as dst:
            for i in range(1, src.count + 1):
                data = src.read(i, resampling=Resampling.nearest)
                dst.write(data, i)
    return corrected_tif_path

# Streamlit UI
st.title('Global Wind Visualization')

# File uploader
uploaded_file = st.file_uploader("Upload a NetCDF file", type=["nc"])

if uploaded_file is not None:
    # Save uploaded file to disk
    with open("uploaded_wind_global.nc", "wb") as f:
        f.write(uploaded_file.getvalue())
    
    filename = "uploaded_wind_global.nc"
    tif_name = "wind_global.tif"
    
    try:
        corrected_tif = convert_netcdf_to_geotiff(filename, tif_name)
        st.success(f"GeoTIFF saved to {corrected_tif}")
        
        # Display the map
        m = Map(layers_control=True)
        m.add_raster(corrected_tif, indexes=[1], palette="coolwarm", layer_name="u_wind")
        geojson = "https://github.com/opengeos/leafmap/raw/master/examples/data/countries.geojson"
        m.add_geojson(geojson, layer_name="Countries")
        m.to_streamlit(height=700)
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.warning("Please upload a file to proceed.")

