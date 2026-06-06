import streamlit as st
import pandas as pd

st.title("Dashboard Kekerasan Perempuan Dewasa")

df = pd.read_csv("dataset/hasil_clustering.csv")

st.write(df.head())