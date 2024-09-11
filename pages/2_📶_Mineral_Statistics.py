import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import leafmap.foliumap as leafmap
from geopy.geocoders import Nominatim

# File paths for all statistics
titanium_export_path = 'data/Titanium Export Statistics.csv'
titanium_import_path = 'data/Titanium Import Statistics.csv'
titanium_production_path = 'data/Titanium Production Statistics.csv'

zirconium_export_path = 'data/Zirconium Export Statistics.csv'
zirconium_import_path = 'data/Zirconium Import Statistics.csv'
zirconium_production_path = 'data/Zirconium Production Statistics.csv'

rare_earth_export_path = 'data/Rare_Earth_Export Statistics.csv'
rare_earth_import_path = 'data/Rare_Earth_Import Statistics.csv'
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

# If no country is selected, display data for top 5 countries with the highest metric tons
if not country_filter:
    top_5_countries = df_filtered.groupby('Country')['Metric Ton'].sum().nlargest(5).index
    df_filtered = df_filtered[df_filtered['Country'].isin(top_5_countries)]

# Filter data by country and sub-commodity if selected
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

st.subheader(f"Trend of {mineral_page} {stat_type} Over Time")

# Increase the width and spacing
line_chart = px.line(df_filtered, x='Year', y='Metric Ton', color='Sub-commodity', 
                     line_group='Country', facet_col='Country', facet_col_wrap=2,  # Two countries per row
                     markers=True, title=f"Trend of {mineral_page} {stat_type} Over Time", 
                     labels={'Metric Ton': 'Amount (Metric Ton)'}, width=1000, height=600)

# Customize layout: hover mode, title font, margins, and spacing between facets
line_chart.update_layout(hovermode='x unified', template='plotly_dark', 
                         title_font=dict(size=24), font=dict(family="Arial", size=14), 
                         margin=dict(l=40, r=40, t=40, b=40), 
                         facet_row_spacing=0.05, facet_col_spacing=0.05)  # Adjust facet spacing

# Display the Plotly line chart in Streamlit
st.plotly_chart(line_chart)


# Initialize the geocoder
geolocator = Nominatim(user_agent="geoapiExercises")

# Function to get lat/lon for a country
def get_country_coordinates(country_name):
    try:
        location = geolocator.geocode(country_name)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        return None, None

# Filter data for selected year
st.subheader(f"Geographical Distribution of {mineral_page} {stat_type}")
year_filter = st.slider('Select Year', min_value=2012, max_value=2022, value=2012)

# Filter the dataframe based on the selected year
df_map = df_filtered[['Country', 'Sub-commodity', str(year_filter)]].copy()
df_map.rename(columns={str(year_filter): 'Metric Ton'}, inplace=True)

# Create the interactive map
m = leafmap.Map(center=[0, 0], zoom=2)

for index, row in df_map.iterrows():
    country = row['Country']
    metric_ton = row['Metric Ton']  # Now using the correct column name for the selected year
    sub_commodity = row['Sub-commodity']
    
    # Get latitude and longitude using geopy
    lat, lon = get_country_coordinates(country)
    
    if lat and lon:
        popup_content = f"{country}<br>Metric Ton: {metric_ton:,}<br>Sub-commodity: {sub_commodity}"
        m.add_marker(location=[lat, lon], popup=popup_content, tooltip=popup_content)

m.to_streamlit(height=500)

# Optionally show raw data
if st.checkbox('Show Raw Data'):
    st.write(df_filtered)
