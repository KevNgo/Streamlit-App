# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 17:04:59 2021

@author: okkev
"""

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import matplotlib.pyplot as plt
import time
import datetime


def log(func):
    def wrapper(*args,**kwargs):
        with open("logProject.txt","a") as f:
            debut = time.time()
            value = func(*args,**kwargs)
            fin = time.time()
            f.write("Called function "+ func.__name__+" loaded in "+str(fin - debut)+"\n")
            return value
    return wrapper

@log
def title():
    st.title('Project Data Visualization - Application ')  

title()   

DATA_URL = (
    "C:\\Users\\okkev\\Projet\\full_2020.csv"
)

st.markdown("<h1 style='text-align: center; color: black;'>Demande valeur foncière</h1>", unsafe_allow_html=True)
st.markdown('<style>h2{color: blue; text-align:center;}</style>', unsafe_allow_html=True)

@log
@st.cache(allow_output_mutation=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data.dropna(subset=["latitude", "longitude"], inplace=True)
    data.drop(data[data['latitude'] == 0].index, inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)

    return data

data = load_data(100000)

@log
@st.cache(suppress_st_warning=True)
def side():

    st.sidebar.header("DVF")
    
    st.sidebar.header("Filter Parameters")

side()


select_map = st.sidebar.selectbox('map', ['','Valeur foncière', 'date_mutation'])

@log
def sidebar_vf():
    st.header("Departments with the highest number of real estate transaction")
    vf = st.sidebar.number_input("Surface terrain en m²", step=1, min_value=0, max_value=1000, value=1)
    st.map(data.query('valeur_fonciere > @vf')[["latitude", "longitude"]])

if select_map == 'Valeur foncière':
    sidebar_vf()

@log
@st.cache(suppress_st_warning=True)
def sidebar_mut(df):  
    st.sidebar.header("date_mutation")
    df["date_mutation"] = pd.to_datetime(df["date_mutation"])
    

    


@log
def hist_st(df):
    fig_wd, ax_wd = plt.subplots()
    ax_wd.hist(df['surface_terrain'], bins=7, rwidth = 0.8, range = (0, 1000),color = "purple")
    ax_wd.set_title('DVF')
    ax_wd.set_xlabel('surface_terrain')
    st.pyplot(fig_wd)

@log
def hist_vf(df):
    fig, ax_wd = plt.subplots()
    ax_wd.hist(df['valeur_fonciere'], bins=7, rwidth = 0.8, range = (0, 1000),color = "blue")
    ax_wd.set_title('DVF')
    ax_wd.set_xlabel('Valeur_Fonciere')
    st.pyplot(fig)


@log
def scatter_vf_df(df):
    fig = px.scatter(
        y = df['valeur_fonciere'],
        x = df['surface_terrain'],
    )
    fig.update_layout(
        xaxis_title="valeur fonciere",
        yaxis_title="surface terrain",
    )

    st.write(fig)
    
    
    
@log
def bar(df):
    fig, ax_wd = plt.subplots()
    ax_wd.hist(df['code_postal'], bins=7, rwidth = 0.8, range = (0, 1000),color = "blue")
    ax_wd.set_title('code_postal')
    ax_wd.set_xlabel('cp')
    st.pyplot(fig)
    
    
    
@log
def pie(df):
    st.subheader('different type de logement')
    
    labels = 'Donées Manquantes', 'Maison', 'Appartement', 'Dépendance', 'Local industriel, commercial ou assimilé'
    
    
    sizes = [41, 21.4, 18, 12.9, 0.37]
    
    explode = (0.05,0.05,0.1,0.1,0.1)
    fig1, ax1 = plt.subplots()

    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=65)
    
    ax1.axis('equal')
    
    st.pyplot(fig1)

@log
def line_chart(df):
    
    fig1, ax1 = plt.subplots()
    
    ax1.plot(df['valeur_fonciere'],df['nom_commune'])

    st.pyplot(fig1)

    
    

if select_map == 'Valeur foncière' or select_map == 'date_mutation': 
    st.sidebar.header("slider figure")
    
    select = st.sidebar.selectbox('', ["", 'Histogram', 'Scatter','Bar','Pie'])
    if select == 'Histogram':
        if st.checkbox("Hist surface terrain"):
            hist_st(data)
        if st.checkbox("Hist valeur fonciere"):
            hist_vf(data)
        
    
    
    
    elif select == 'Scatter':
        if st.checkbox("Scatter"):
            scatter_vf_df(data)
        if st.checkbox("Line"):
            line_chart(data)
        
    
    elif select == 'Bar':
        if st.checkbox('Bar'):
            bar(data)
            
    elif select =='Pie':
        if st.checkbox('Pie'):
            pie(data)
     
    if select == 'Histogram' or select == 'Scatter' or select == 'Bar' or select == 'Pie':
        st.sidebar.markdown("libraries used: **streamlit**, **pandas**, **numpy**, **plotly**")
        st.sidebar.markdown("**Dataset:** Rows: 2.45M  Columns: 40")
        st.sidebar.markdown("Update: Octobre, 2021")
