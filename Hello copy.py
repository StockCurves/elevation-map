# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

import matplotlib.pyplot as plt
import gpxpy
import geopy


import matplotlib.pyplot as plt
from matplotlib import rcParams

import matplotlib.font_manager as mpfm
import os

# Set Font
@st.cache_data 
def fontRegistered():
    font_dirs = [os.getcwd() + '/font']
    font_files = mpfm.findSystemFonts(fontpaths=font_dirs)
    st.write(font_dirs)
    for font_file in font_files:
        st.write(font_file)
        mpfm.fontManager.addfont(font_file)
        prop = mpfm.FontProperties(fname=font_file)
    # mpfm._load_fontmanager(try_read_cache=False)
    # font_dirs = ['/my/custom/font/dir', ]
    # font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    # font_list = mpfm.createFontList(font_files)
    # mpfm.fontManager.ttflist.extend(font_list)
    # prop = font_manager.FontProperties(fname=font_dirs)

# mpfm.addfont('./font/SimHei.ttf')
# plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
# mpfm.fontManager.addfont('./font/NotoSansTC-Regular.ttf')
# mpfm.fontManager.addfont('./font/Microsoft-JhengHei.ttf')
# plt.rcParams['font.sans-serif'] = ['NotoSansTC-Regular', 'Microsoft-JhengHei'] 
# plt.rcParams['axes.unicode_minus'] = False
# rcParams["font.size"]= 20
# matplotlib.rc('font', family='SimHei')

LOGGER = get_logger(__name__)

def get_elevation(gpx):
    import math
    from geopy import distance 

    yk_lat   = []
    yk_lon   = []
    yk_ele0  = [] # gpx elevation
    yk_ele1  = [] # SRTM elevation from NASA
    dis_flat = [] # spherical distance
    dis_eucl = [] # euclidian /b surface distance

    for segment in gpx.tracks[0].segments:
        for p in segment.points:     
            lat = p.latitude
            lon = p.longitude
            yk_lat.append(lat)
            yk_lon.append(p.longitude)
            yk_ele0.append(p.elevation)
            
    dis_sum_flat = []
    dis_sum_eucl = []
    s = 0
    s1 = 0

    # point-to-point distance
    for i, x in enumerate(yk_lat[1:], 1):
        p1 = (yk_lat[i-1], yk_lon[i-1])
        p2 = (yk_lat[i], yk_lon[i])    
        dis = distance.distance(p1, p2).km
        dis_flat.append( dis )
        dis_eucl.append( math.sqrt(dis**2 + (yk_ele0[i]/1000 - yk_ele0[i-1]/1000)**2) )

    # cumulated sum    
    for i, d in enumerate(dis_flat):    
        s += dis_flat[i]
        s1 += dis_eucl[i]
        dis_sum_flat.append(s)
        dis_sum_eucl.append(s1)

    return [dis_sum_flat, yk_ele0[1:]]

def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to Streamlit! 👋")
    # st.sidebar.success("Select a demo above.")
    st.markdown(
        """
          test
        """
    )
    # st.markdown(
    #     """
    #     <style>
    #     @font-face {
    #       font-family: 'Tangerine';
    #       font-style: normal;
    #       font-weight: 12;
    #       src: url(https://fonts.gstatic.com/s/tangerine/v12/IurY6Y5j_oScZZow4VOxCZZM.woff2) format('woff2');
    #       unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
    #     }
    #         html, body, [class*="css"]  {
    #         font-family: 'Tangerine';
    #         font-size: 48px;
    #         }
    #         </style>
    #         """,
    #             unsafe_allow_html=True,
    # )

    fontRegistered()
    plt.rcParams['font.sans-serif'] = ['NotoSansTC-Regular', 'Microsoft-JhengHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    rcParams["font.size"]= 20

    # Create a list to store uploaded files
    uploaded_files = []
    uploaded_files = st.file_uploader("Upload files", type=["gpx"], accept_multiple_files=True)

    # Display uploaded files and provide a delete option
    # if uploaded_files:
    #     st.header("Uploaded Files:")
    #     for file in uploaded_files:
    #         file_name = file.name
    #         # Display file name
    #         st.write(file_name)
    #         # Create a button to delete the file
    #         if st.button(f"Delete {file_name}"):
    #             uploaded_files.remove(file)
    #             st.success(f"{file_name} has been deleted.")
                # Optional: You can also delete the file from the server if needed.
                # os.remove(file_name)

    # Display the uploaded files
    st.subheader("Maps of the Elvation:")
    fig, d1 = plt.subplots(1,1)
    fig.set_figheight(12)
    fig.set_figwidth(15)

    data_ = {}
    for fn in uploaded_files:
        # st.write(fn.name)
        fn = fn.name
        with open(fn) as f:
            gpx = gpxpy.parse(f)       
        [d, e0] = get_elevation(gpx)
        d1.plot(d, e0, lw=5, label = fn.split('.')[0])   
        data[fn, d, e0] 

    d1.set_xlabel("距離 (KM)")
    d1.set_ylabel("海跋 (M)")
    d1.legend();
    d1.grid()        

    st.pyplot(fig)        
      


if __name__ == "__main__":
    run()

