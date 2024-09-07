import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# Step 1: Load Data
file_path = "data/Global Mineral Mining Stations.csv"
data = pd.read_csv(file_path)

# Step 2: Streamlit Page Setup
st.set_page_config(page_title="Global Mineral Mining Dashboard", layout="wide")

st.title("Global Mineral Mining Dashboard")
st.markdown("Explore global mineral mining deposit locations, critical minerals, and deposit types.")

# Step 3: Filters
with st.container():
    left, middle, right = st.columns(3)
    with left:
        country_filter = st.selectbox('Select Country', options=['All'] + sorted(data['LOCATION'].unique().tolist()))
    with middle:
        critical_mineral_filter = st.multiselect('Select Critical Minerals', options=sorted(data['CRITICAL_M'].dropna().unique().tolist()))
    with right:
        deposit_type_filter = st.selectbox('Select Deposit Type', options=['All'] + sorted(data['DEPOSIT_TY'].unique().tolist()))

    st.caption("Filter data using the dropdowns above.")

# Step 4: Data Filtering
filtered_data = data.copy()

if country_filter != 'All':
    filtered_data = filtered_data[filtered_data['LOCATION'] == country_filter]

if len(critical_mineral_filter) > 0:
    filtered_data = filtered_data[filtered_data['CRITICAL_M'].isin(critical_mineral_filter)]

if deposit_type_filter != 'All':
    filtered_data = filtered_data[filtered_data['DEPOSIT_TY'] == deposit_type_filter]

# Step 5: Map Creation
m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB positron")

# Add Marker Cluster
marker_cluster = MarkerCluster().add_to(m)

# Step 6: Add Markers to Map
for _, row in filtered_data.iterrows():
    popup_text = f"""
    <b>Deposit Name:</b> {row['DEPOSIT_NA']}<br>
    <b>Location:</b> {row['LOCATION']} - {row['LOC_DETAIL']}<br>
    <b>Critical Minerals:</b> {row['CRITICAL_M']}<br>
    <b>Deposit Type:</b> {row['DEPOSIT_TY']}
    """
    folium.Marker(
        location=[row['LATITUDE'], row['LONGITUDE']],
        popup=popup_text,
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(marker_cluster)

# Step 7: Display Map
st_folium(m, width=1000, height=500)

# Display the filtered data as a table
st.write("Filtered Data:", filtered_data)
