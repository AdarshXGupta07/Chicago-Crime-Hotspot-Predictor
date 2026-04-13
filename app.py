
import streamlit as st
import folium
from folium.plugins import HeatMap
import pandas as pd
import pickle
from streamlit_folium import st_folium

# Model load karo
with open('crime_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('label_encoder.pkl', 'rb') as f:
    le = pickle.load(f)

# Data load karo
df = pd.read_csv('Chicago_Crimes_2012_to_2017.csv')
df = df[['Primary Type', 'Latitude', 'Longitude', 'Year']].dropna()

st.title("🗺️ Chicago Crime Hotspot Predictor")
st.write("Real crime data se banaya gaya!")

# Sidebar filters
st.sidebar.header("Filters")
year = st.sidebar.slider("Year", 2012, 2017, 2015)
crime_type = st.sidebar.selectbox("Crime Type", df['Primary Type'].unique())

# Filter data
filtered = df[(df['Year'] == year) & (df['Primary Type'] == crime_type)]
st.write(f"Total crimes: {len(filtered)}")

# Map banao
chicago_map = folium.Map(location=[41.8781, -87.6298], zoom_start=11)
heat_data = filtered[['Latitude', 'Longitude']].values.tolist()
HeatMap(heat_data, radius=10).add_to(chicago_map)

# Map dikhao
st_folium(chicago_map, width=700, height=500)

# Top areas
st.subheader("📊 Crime Stats")
st.bar_chart(df[df['Year']==year]['Primary Type'].value_counts().head(10))
