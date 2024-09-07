import pandas as pd
import plotly.express as px
import streamlit as st

# Load the data
data_path = 'data/global_mining_area_per_country_v2.csv'
df = pd.read_csv(data_path)

# Clean the column names: Strip whitespace from the names
df.columns = df.columns.str.strip()

# Initialize the Streamlit app
st.title("Global Mining Area Dashboard")

# Sidebar filters
country_filter = st.sidebar.multiselect('Select Countries', options=df['COUNTRY_NAME'].unique(), default=df['COUNTRY_NAME'].unique())

# Filter the dataframe based on selections
df_filtered = df[df['COUNTRY_NAME'].isin(country_filter)]

# Display raw data if needed
if st.checkbox('Show Raw Data'):
    st.write(df_filtered)

# Choropleth Map: Geographical Visualization of Mining Area
st.subheader("Choropleth Map: Total Mining Area by Country")

# Plotly Choropleth Map
choropleth_map = px.choropleth(df_filtered, 
                               locations="ISO3_CODE", 
                               locationmode="ISO-3",
                               color="AREA",
                               hover_name="COUNTRY_NAME",
                               color_continuous_scale=px.colors.sequential.Plasma,
                               labels={'AREA': 'Mining Area (sq km)'},
                               title="Mining Area (sq km) by Country")

st.plotly_chart(choropleth_map)


# Maximum and Minimum Mining Area by Country
st.subheader("Maximum and Minimum Mining Area by Country")

# Maximum and Minimum Calculations
max_area = df_filtered.loc[df_filtered['AREA'].idxmax()]
min_area = df_filtered.loc[df_filtered['AREA'].idxmin()]

st.write(f"**Country with Maximum Mining Area**: {max_area['COUNTRY_NAME']} - {max_area['AREA']} sq km")
st.write(f"**Country with Minimum Mining Area**: {min_area['COUNTRY_NAME']} - {min_area['AREA']} sq km")

# Bar Chart: Top 10 Countries by Mining Area
st.subheader("Top 10 Countries by Mining Area")
top10_countries = df_filtered.nlargest(10, 'AREA')

bar_chart = px.bar(top10_countries, 
                   x='COUNTRY_NAME', 
                   y='AREA', 
                   labels={'AREA': 'Mining Area (sq km)'}, 
                   title="Top 10 Countries by Mining Area",
                   color='COUNTRY_NAME')
st.plotly_chart(bar_chart)

# Scatter Plot: Relationship Between Mining Area and Number of Features
st.subheader("Mining Area vs Number of Features")
scatter_plot = px.scatter(df_filtered, 
                          x='AREA', 
                          y='N_FEATURES', 
                          labels={'AREA': 'Mining Area (sq km)', 'N_FEATURES': 'Number of Mining Features'},
                          title="Mining Area vs Number of Features by Country", 
                          hover_name="COUNTRY_NAME",
                          color="COUNTRY_NAME")
st.plotly_chart(scatter_plot)

# Statistical Summary
st.subheader("Statistical Summary of Mining Areas")
st.write(f"**Average Mining Area**: {df_filtered['AREA'].mean():.2f} sq km")
st.write(f"**Total Mining Area (Global)**: {df_filtered['AREA'].sum():.2f} sq km")
