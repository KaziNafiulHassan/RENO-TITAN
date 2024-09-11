import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# File paths for all statistics
titanium_export_path = 'data/Titanium Export Statistics.csv'
titanium_import_path = 'data/Titanium Import Statistics.csv'
titanium_production_path = 'data/Titanium Production Statistics.csv'

zirconium_export_path = 'data/Zirconium Export Statistics.csv'
zirconium_import_path = 'data/Zirconium Import Statistics.csv'
zirconium_production_path = 'data/Zirconium Production Statistics.csv'

rare_earth_export_path = 'data/Rare_Earth_Export_Statistics.csv'
rare_earth_import_path = 'data/Rare_Earth_Import_Statistics.csv'
rare_earth_production_path = 'data/Rare_Earth_Production_Statistics.csv'

# Function to load and preprocess the data
def load_and_clean_data(data_path):
    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip()  # Clean column names by stripping whitespace
    df_cleaned = df.dropna(subset=[str(year) for year in range(2012, 2022)], how='all')  # Clean rows with NaN values
    df_melted = df_cleaned.melt(id_vars=['Country', 'Sub-commodity'], var_name='Year', value_name='Metric Ton')
    return df_melted

# Sidebar for mineral selection and statistics type
st.sidebar.title("Mineral Statistics")
mineral_page = st.sidebar.radio("Select Mineral", ["Titanium", "Zirconium", "Rare Earth"])

st.sidebar.title("Select Statistic Type")
stat_type = st.sidebar.radio("Statistic Type", ["Export", "Import", "Production"])

# Load data based on mineral and statistic type
if mineral_page == "Titanium":
    st.title(f"Interactive Dashboard: Titanium {stat_type} Statistics")
    if stat_type == "Export":
        df_filtered = load_and_clean_data(titanium_export_path)
    elif stat_type == "Import":
        df_filtered = load_and_clean_data(titanium_import_path)
    else:
        df_filtered = load_and_clean_data(titanium_production_path)
        
elif mineral_page == "Zirconium":
    st.title(f"Interactive Dashboard: Zirconium {stat_type} Statistics")
    if stat_type == "Export":
        df_filtered = load_and_clean_data(zirconium_export_path)
    elif stat_type == "Import":
        df_filtered = load_and_clean_data(zirconium_import_path)
    else:
        df_filtered = load_and_clean_data(zirconium_production_path)
        
else:
    st.title(f"Interactive Dashboard: Rare Earth {stat_type} Statistics")
    if stat_type == "Export":
        df_filtered = load_and_clean_data(rare_earth_export_path)
    elif stat_type == "Import":
        df_filtered = load_and_clean_data(rare_earth_import_path)
    else:
        df_filtered = load_and_clean_data(rare_earth_production_path)

# Filter data based on country and sub-commodity selections
st.subheader(f"Filter Data for {mineral_page} {stat_type}")
country_filter = st.multiselect('Select Countries', options=df_filtered['Country'].unique())
commodity_filter = st.multiselect('Select Sub-commodities', options=df_filtered['Sub-commodity'].unique())

if country_filter:
    df_filtered = df_filtered[df_filtered['Country'].isin(country_filter)]
if commodity_filter:
    df_filtered = df_filtered[df_filtered['Sub-commodity'].isin(commodity_filter)]

# Display maximum value for the selected data
st.subheader(f"Maximum {stat_type} for {mineral_page}")
max_value = df_filtered['Metric Ton'].max()
max_row = df_filtered[df_filtered['Metric Ton'] == max_value]
st.metric(label=f"Maximum {stat_type} (Metric Ton)", value=f"{max_value:,}")
st.write(f"Country: {max_row.iloc[0]['Country']}, Sub-commodity: {max_row.iloc[0]['Sub-commodity']}, Year: {max_row.iloc[0]['Year']}")

# Create charts for the selected mineral and statistic
st.subheader(f"Trend of {mineral_page} {stat_type} Over Time")
line_chart = px.line(df_filtered, x='Year', y='Metric Ton', color='Country', line_group='Sub-commodity', markers=True, 
                     title=f"Trend of {mineral_page} {stat_type} Over Time", 
                     labels={'Metric Ton': 'Amount (Metric Ton)'})
line_chart.update_layout(hovermode='x unified', template='plotly_dark', title_font=dict(size=24), 
                         font=dict(family="Arial", size=14))
st.plotly_chart(line_chart)

st.subheader(f"Comparison of {mineral_page} {stat_type} by Country and Sub-commodity")
bar_chart = px.bar(df_filtered, x='Country', y='Metric Ton', color='Sub-commodity', barmode='group', 
                   title=f"Comparison of {mineral_page} {stat_type} by Country and Sub-commodity")
bar_chart.update_layout(hovermode='x unified', template='plotly_dark', title_font=dict(size=24),
                        font=dict(family="Arial", size=14))
st.plotly_chart(bar_chart)

# Choropleth map for geographical distribution
st.subheader(f"Geographical Distribution of {mineral_page} {stat_type}")
year_filter = st.slider('Select Year', min_value=2012, max_value=2022, value=2012)
df_choropleth = df_filtered[df_filtered['Year'] == str(year_filter)]
choropleth_map = px.choropleth(df_choropleth, locations="Country", locationmode='country names', 
                               color="Metric Ton", hover_name="Country", 
                               color_continuous_scale=px.colors.sequential.Plasma,
                               title=f"Geographical Distribution of {mineral_page} {stat_type} in {year_filter}")
choropleth_map.update_layout(template='plotly_dark', title_font=dict(size=24), 
                             font=dict(family="Arial", size=14))
st.plotly_chart(choropleth_map)

# Optionally show raw data
if st.checkbox('Show Raw Data'):
    st.write(df_filtered)
