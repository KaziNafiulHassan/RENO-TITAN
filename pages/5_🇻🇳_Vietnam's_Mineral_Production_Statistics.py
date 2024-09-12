import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
df = pd.read_csv("data/Vietnam Statistical Yearbook Data.csv")

# Data cleaning
df = df.dropna(how='all')  # Drop rows where all values are NaN
df.fillna(0, inplace=True)  # Fill missing values with 0 for simplicity

# List of minerals/resources for analysis
minerals = ["Titan ores", "Coal", "Iron ores", "Copper ores", "Antimoan ores",
            "Stone of all kinds", "Sands", "Pebbles, gravel", "Apatite ores", "Lime", "Sand, Pebbles"]

# Streamlit page setup
st.title("Vietnam Mineral Production Statistics")

# Sidebar for selecting visualization type
st.sidebar.title("Visualization Options")
plot_type = st.sidebar.selectbox("Choose the type of plot", ["Line Charts", "Bar Charts", "Stacked Area Charts", "Heatmaps", "Box Plots", "Facet Grids"])

# Sidebar for selecting minerals and year range
selected_minerals = st.sidebar.multiselect("Select Minerals", minerals, default=minerals)
selected_years = st.sidebar.slider("Select Year Range", int(df['Year'].min()), int(df['Year'].max()), (int(df['Year'].min()), int(df['Year'].max())))

# Filter the data based on user selections
df_filtered = df[(df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]
df_filtered = df_filtered[['Year'] + selected_minerals]

# Plot 1: Line Chart - Production Trends Over Time
if plot_type == "Line Charts":
    st.subheader("Production Trends of Selected Minerals Over Time")
    line_chart = px.line(df_filtered.melt(id_vars='Year', var_name='Mineral', value_name='Production'),
                         x='Year', y='Production', color='Mineral', title="Mineral Production Trends Over Time")
    st.plotly_chart(line_chart)

# Plot 2: Bar Chart - Compare Mineral Production by Year
elif plot_type == "Bar Charts":
    st.subheader("Comparison of Mineral Production for Selected Year")
    selected_year = st.sidebar.selectbox("Select Year for Bar Chart", df_filtered['Year'].unique())
    df_year = df_filtered[df_filtered['Year'] == selected_year].set_index('Year').T.reset_index().rename(columns={'index': 'Mineral', selected_year: 'Production'})
    bar_chart = px.bar(df_year, x='Mineral', y='Production', title=f"Mineral Production in {selected_year}")
    st.plotly_chart(bar_chart)

# Plot 3: Stacked Area Chart - Contributions to Total Production Over Time
elif plot_type == "Stacked Area Charts":
    st.subheader("Contributions of Minerals to Total Production Over Time")
    stacked_area_chart = px.area(df_filtered.melt(id_vars='Year', var_name='Mineral', value_name='Production'),
                                 x='Year', y='Production', color='Mineral', title="Total Production Contributions")
    st.plotly_chart(stacked_area_chart)

# Plot 4: Heatmap - Correlation Between Mineral Productions
elif plot_type == "Heatmaps":
    st.subheader("Correlation Between Mineral Production Levels")
    df_corr = df_filtered.drop(columns='Year').corr()
    fig, ax = plt.subplots()
    sns.heatmap(df_corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

# Plot 5: Box Plot - Distribution of Production Data for Each Mineral
elif plot_type == "Box Plots":
    st.subheader("Statistical Distribution of Production Data for Each Mineral")
    box_plot = px.box(df_filtered.melt(id_vars='Year', var_name='Mineral', value_name='Production'),
                      x='Mineral', y='Production', title="Distribution of Mineral Production")
    st.plotly_chart(box_plot)

# Plot 6: Facet Grids - Individual Trends for Each Mineral
elif plot_type == "Facet Grids":
    st.subheader("Facet Grid of Production Trends for Each Mineral")
    facet_grid = px.line(df_filtered.melt(id_vars='Year', var_name='Mineral', value_name='Production'),
                         x='Year', y='Production', facet_col='Mineral', facet_col_wrap=2, title="Facet Grid of Mineral Production Trends")
    st.plotly_chart(facet_grid)

# Add some footer information
st.write("### Data Source: Vietnam Statistical Yearbook Data")
st.write("### Analysis by Kazi Nafiul Hassan - 2024")
