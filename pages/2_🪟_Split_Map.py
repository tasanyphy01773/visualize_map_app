import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("Split-panel Map")

tif_path = 'https://github.com/tasanyphy01773/visualize_map_app/releases/download/dataset/wind_global_corrected.tif'

# Open the GeoTIFF file
with rasterio.open(tif_path) as src:
    # Read the data
    u_wind = src.read(1)  # Read the first band

    v_wind = src.read(2)

with st.expander("See source code"):
    with st.echo():
        m = leafmap.Map()
        # before = 'https://github.com/tasanyphy01773/visualize_map_app/releases/download/dataset/wind_global_corrected.tif'
        m.split_map(
            left_layer=u_wind, right_layer=v_wind
        )
        m.add_legend(title="ESA Land Cover", builtin_legend="ESA_WorldCover")

m.to_streamlit(height=700)
