#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 09:50:57 2023

@author: ellisobrien
"""

#data processing and manipulatation packages
import pandas as pd
import numpy as np
from urllib.request import urlopen
import json

#visualization packages
import plotly.express as px
import plotly 

#dashboard package
import streamlit as st


#Writing dashboard title 
st.title("Visualizing Natural Disaster Risk and Climate Risk in the U.S.)

#Adding text describing issue 
st.write('Natural disasters present a fundamental risk to housing and economic security in the U.S. In 2021 alone natural disasters cost the U.S $145 Billion. In an effort to improve data surrounding natural disasters, the Federal Emergency Management Agency released the National Risk Index (NRI) which provides comprehensive county level data on natural disaster risks.')


st.write('This tool is intended for policy makers, academics, and students who may use it to generate low code visualizations to understanding of geospatial risk in the country or their state.')


#imporing json 
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    county = json.load(response)
    
#importing data from github
NRI=pd.read_csv('https://raw.githubusercontent.com/ellisobrien/NRI_Viz_Library/main/NRI_Table_Counties.csv', dtype={"STCOFIPS": str})

#renaming county fips code
NRI.rename(columns={'STCOFIPS':'FIPS'}, inplace=True)



st.header('Identifying High Risk States')

#section desrciption
st.write("This section provides a high level understanding of loss and risk for each state analyzed.")


#selecting key states for scatter plot
nri_plot_1=NRI[['STATEABBRV', 'EAL_VALB', "EAL_VALA", "EAL_VALPE"]]

#summinng features
nri_plot_1=nri_plot_1.groupby('STATEABBRV').sum()

#making state a coumumn
nri_plot_1.reset_index(inplace=True)

#sorting data for plot
nri_plot_1=nri_plot_1.sort_values(by=['EAL_VALB'], ascending=False)

#renaming columns
nri_plot_1.rename(columns={'EAL_VALB': 'Building Loss',
                         'EAL_VALA': 'Agricultural Loss',
                         'EAL_VALPE': 'Population Loss'},
                                           inplace=True)

#making bar graph
fig0 = px.bar(nri_plot_1, x="STATEABBRV", 
             y=['Building Loss', 'Agricultural Loss', 'Population Loss'], 
             labels={"value": "Annual Estimated Loss ($)", 'STATEABBRV':'State', "variable": "Loss Breakdown"},
             color_discrete_map={"Building Loss": "silver", "Agricultural Loss": "green", 'Population Loss':'black'},
             template="simple_white",
             height=400)
fig0.update_layout(title_text = '<b>Figure 1: State Level Loss Broken Down by Loss Type </b> <br><sup> California and Texas Lead All States in Loss </sup>')

#displaying viz
st.plotly_chart(fig0)