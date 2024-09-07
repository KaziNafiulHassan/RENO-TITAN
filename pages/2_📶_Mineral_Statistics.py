import pandas as pd
import plotly.express as px
import streamlit as st

# Load the CSV from the local path
data_path = 'data/Titanium Export Statistics.csv'
df = pd.read_csv(data_path)

# Clean the column names: Strip whitespace from the names
df.columns = df.columns.str.strip()

# Clean the data: Drop rows with all NaN values across the years (1970-2000)
df_cleaned = df.dropna(subset=[str(year) for year in range(1970, 2001)], how='all')

# Melt the dataframe to make it easier for plotting
df_melted = df_cleaned.melt(id_vars=['Country', 'Sub-commodity'], var_name='Year', value_name='Export in Metric Ton')

# Initialize a Streamlit app
st.title("Interactive Dashboard: Titanium Export Statistics (1970-2000)")

# Sidebar filter
country_filter = st.sidebar.multiselect('Select Countries', options=df_melted['Country'].unique(), default=df_melted['Country'].unique())
commodity_filter = st.sidebar.multiselect('Select Sub-commodities', options=df_melted['Sub-commodity'].unique(), default=df_melted['Sub-commodity'].unique())
year_filter = st.sidebar.slider('Select Year', min_value=1970, max_value=2000, value=1970)

# Filter the dataframe based on selections
df_filtered = df_melted[(df_melted['Country'].isin(country_filter)) & (df_melted['Sub-commodity'].isin(commodity_filter))]

# Line Chart: Trend over Time
st.subheader("Trend of Titanium Exports Over Time")
line_chart = px.line(df_filtered, x='Year', y='Export in Metric Ton', color='Country', line_group='Sub-commodity', markers=True, title="Trend of Titanium Exports (1970-2000)")
st.plotly_chart(line_chart)

# Bar Chart: Value by Country and Commodity
st.subheader("Comparison of Titanium Exports by Country and Commodity")
bar_chart = px.bar(df_filtered, x='Country', y='Export in Metric Ton', color='Sub-commodity', barmode='group', title="Comparison by Country and Sub-commodity")
st.plotly_chart(bar_chart)

# Maximum and Minimum Export by Country
st.subheader("Maximum and Minimum Exports by Country")

# Group data by country and find max/min exports
df_grouped = df_melted.groupby('Country')['Export in Metric Ton'].agg(['max', 'min']).reset_index()

# Display maximum and minimum exports
st.write("Maximum Exports by Country")
st.write(df_grouped[['Country', 'max']].sort_values(by='max', ascending=False))

st.write("Minimum Exports by Country")
st.write(df_grouped[['Country', 'min']].sort_values(by='min'))

# Choropleth Map: Geographical Distribution of Values
st.subheader("Geographical Distribution of Titanium Exports")
df_choropleth = df_filtered[df_filtered['Year'] == str(year_filter)]
choropleth_map = px.choropleth(df_choropleth, locations="Country", locationmode='country names', 
                               color="Export in Metric Ton", hover_name="Country", 
                               color_continuous_scale=px.colors.sequential.Plasma, 
                               title=f"Geographical Distribution for {year_filter}")
st.plotly_chart(choropleth_map)

# Show raw data if needed
if st.checkbox('Show Raw Data'):
    st.write(df_filtered)
