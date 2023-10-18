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

# import matplotlib.pyplot as plt
import gpxpy
# import geopy

import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px


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
    points = []
    for i, d in enumerate(dis_flat):    
        s += dis_flat[i]
        s1 += dis_eucl[i]
        dis_sum_flat.append(s)
        dis_sum_eucl.append(s1)
        points.append(
            {
                "d": s,
                "e": yk_ele0[i]
            }
        )

    return [dis_sum_flat, yk_ele0[1:]]
    # return points

def get_gpx_files():
    uploaded_files = [] # '桶後越嶺步道.gpx'
    gpx_files = st.file_uploader("請上傳多個.gpx檔", type=["gpx"], accept_multiple_files=True)
    return gpx_files

def create_traces(gpx_files):
    traces = []

    for f in gpx_files:
        fn = f.name
        with open(fn) as gpxf:
            gpx = gpxpy.parse(gpxf)       
        [d, e0] = get_elevation(gpx)
        traces.append({
            "isShown": st.checkbox(f.name, True),
            "trace": go.Scatter(x=d, y=e0, mode='lines', name=fn.split('.')[0])
        })
    return traces

def create_map(traces):
    new_traces = [x["trace"] for x in traces if x['isShown']]
    layout = go.Layout(title='海拔地圖', xaxis=dict(title='距離[KM]'), yaxis=dict(title='高度[M]'))

    fig = go.Figure(data=new_traces, layout=layout)
    st.plotly_chart(fig, use_container_width=True)

def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )
    st.write("# Welcome to Streamlit! 👋")

    gpx_files = get_gpx_files()
    traces = create_traces(gpx_files)
    create_map(traces)
    
if __name__ == "__main__":
    run()

