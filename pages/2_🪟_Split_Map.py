import streamlit as st
import leafmap.foliumap as leafmap
import os
import requests

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

# Function to download the file
def download_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    else:
        return False

# URL and filename for the GeoTIFF
url = 'https://github.com/tasanyphy01773/visualize_map_app/releases/download/dataset/wind_global_corrected.tif'
filename = 'wind_global_corrected.tif'

# Check if the file already exists, if not, download it
if not os.path.exists(filename):
    result = download_file(url, filename)
    if not result:
        st.error('Failed to download file. Please check the URL or network settings.')

with st.expander("See source code"):
    with st.echo():
        m = leafmap.Map()
        # Add the two indices of the GeoTIFF file to the map
        m.add_raster(filename, layer_name="U-Wind Data 1", palette="coolwarm", band=1)
        m.add_raster(filename, layer_name="U-Wind Data 2", palette="coolwarm", band=2)

        # Use split-map functionality
        m.split_map(
            left_layer="U-Wind Data 1", right_layer="U-Wind Data 2"
        )
        m.add_legend(title="ESA Land Cover", builtin_legend="ESA_WorldCover")

# Display the map in Streamlit
m.to_streamlit(height=700)








# import streamlit as st
# import leafmap.foliumap as leafmap

# st.set_page_config(layout="wide")

# markdown = """
# A Streamlit map template
# <https://github.com/opengeos/streamlit-map-template>
# """

# st.sidebar.title("About")
# st.sidebar.info(markdown)
# logo = "https://i.imgur.com/UbOXYAU.png"
# st.sidebar.image(logo)

# st.title("Split-panel Map")



# with st.expander("See source code"):
#     with st.echo():
#         m = leafmap.Map()
#         before = 'https://github.com/tasanyphy01773/visualize_map_app/releases/download/dataset/wind_global_corrected.tif'

#         m.split_map(
#             left_layer=before, right_layer="ESA WorldCover 2020"
#         )
#         m.add_legend(title="ESA Land Cover", builtin_legend="ESA_WorldCover")

# m.to_streamlit(height=700)
