import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
import streamlit as st

def create_choropleth_map(df, geo_json, locations_col, color_col, title, color_scale='Viridis'):
    """
    Creates a choropleth map using Plotly.
    
    Args:
        df (pandas.DataFrame): Data containing locations and values
        geo_json (dict): GeoJSON data for map boundaries
        locations_col (str): Column name in df that matches GeoJSON feature.id
        color_col (str): Column name in df for color intensity
        title (str): Map title
        color_scale (str): Color scale for the map
        
    Returns:
        plotly.graph_objects.Figure: Choropleth map figure
    """
    fig = px.choropleth(
        df,
        geojson=geo_json,
        locations=locations_col,
        color=color_col,
        color_continuous_scale=color_scale,
        title=title
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    return fig

def create_time_series(df, x_col, y_col, title, color=None, labels=None):
    """
    Creates a time series line chart using Plotly.
    
    Args:
        df (pandas.DataFrame): Data containing time series
        x_col (str): Column name for x-axis (typically dates)
        y_col (str): Column name for y-axis values
        title (str): Chart title
        color (str, optional): Column name for color differentiation
        labels (dict, optional): Custom axis labels
        
    Returns:
        plotly.graph_objects.Figure: Line chart figure
    """
    if labels is None:
        labels = {}
    
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        color=color,
        title=title,
        labels=labels
    )
    fig.update_layout(margin={"r":10,"t":30,"l":10,"b":10})
    return fig

def create_folium_map(center=[20.5937, 78.9629], zoom=5):
    """
    Creates a Folium map centered on India.
    
    Args:
        center (list): Center coordinates [lat, lon]
        zoom (int): Initial zoom level
        
    Returns:
        folium.Map: Folium map object
    """
    m = folium.Map(location=center, zoom_start=zoom, tiles="OpenStreetMap")
    return m

def add_markers_to_map(m, df, lat_col, lon_col, popup_col, tooltip_col=None, color='blue'):
    """
    Adds markers to a Folium map from DataFrame coordinates.
    
    Args:
        m (folium.Map): Folium map object
        df (pandas.DataFrame): Data containing coordinates and popup info
        lat_col (str): Column name for latitude
        lon_col (str): Column name for longitude
        popup_col (str): Column name for popup content
        tooltip_col (str, optional): Column name for tooltip content
        color (str): Marker color
        
    Returns:
        folium.Map: Map with markers added
    """
    for idx, row in df.iterrows():
        tooltip = row[tooltip_col] if tooltip_col else None
        folium.Marker(
            location=[row[lat_col], row[lon_col]],
            popup=row[popup_col],
            tooltip=tooltip,
            icon=folium.Icon(color=color)
        ).add_to(m)
    return m