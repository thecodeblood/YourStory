import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import folium_static
import os
import plotly.graph_objects as go
from utils.visualization import create_choropleth_map, create_time_series, create_folium_map, add_markers_to_map

# Initialize session state for favorites
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# Function to load data
def load_data():
    """Load processed data for visualization"""
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'processed')
    
    data = {}
    
    # Tourism Statistics
    tourism_file = os.path.join(data_dir, 'tourism_statistics_processed.csv')
    if os.path.exists(tourism_file):
        data['tourism'] = pd.read_csv(tourism_file)
    
    # Cultural Sites
    sites_file = os.path.join(data_dir, 'cultural_sites_processed.csv')
    if os.path.exists(sites_file):
        data['sites'] = pd.read_csv(sites_file)
    
    # Art Forms
    art_file = os.path.join(data_dir, 'art_forms_processed.csv')
    if os.path.exists(art_file):
        data['art'] = pd.read_csv(art_file)
    
    # Government Funding
    funding_file = os.path.join(data_dir, 'government_funding_processed.csv')
    if os.path.exists(funding_file):
        data['funding'] = pd.read_csv(funding_file)
    
    return data

# Load data
data = load_data()

# Page configuration
st.set_page_config(
    page_title="Indian Cultural Heritage & Tourism",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("Exploring India's Cultural Heritage & Tourism")

# Horizontal Navigation Bar
st.markdown("""
<style>
    .nav-container {
        display: flex;
        justify-content: space-between;
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .nav-item {
        padding: 8px 16px;
        text-align: center;
        border-radius: 4px;
    }
    .nav-item:hover {
        background-color: #e0e2e6;
    }
</style>
""", unsafe_allow_html=True)

# Create a row for the navigation buttons
col1, col2, col3, col4, col5 = st.columns(5)

# Set default page if not in session state
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# Navigation buttons
with col1:
    if st.button("Home", key="home_btn", use_container_width=True):
        st.session_state.page = "Home"

with col2:
    if st.button("Art Forms Explorer", key="art_btn", use_container_width=True):
        st.session_state.page = "Art Forms Explorer"

with col3:
    if st.button("Cultural Tourism", key="tourism_btn", use_container_width=True):
        st.session_state.page = "Cultural Tourism Analysis"

with col4:
    if st.button("Government Initiatives", key="gov_btn", use_container_width=True):
        st.session_state.page = "Government Initiatives"

with col5:
    if st.button("Responsible Tourism", key="resp_btn", use_container_width=True):
        st.session_state.page = "Responsible Tourism"

# Add a separator after navigation
st.markdown("<hr>", unsafe_allow_html=True)

# Introduction content
st.markdown("""
    <div style='background-color: #f5f5f5; padding: 20px; border-radius: 10px;'>
    <h3>Discover the Rich Cultural Tapestry of India</h3>
    <p>This application showcases traditional art forms, cultural experiences, and tourism trends across India.
    Explore the data-driven insights into India's artistic and cultural heritage, and discover opportunities for responsible tourism.</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar customization
st.sidebar.title("Customization")
theme = st.sidebar.radio(
    "Select Theme",
    ["Light", "Dark"]
)

# Apply theme
if theme == "Dark":
    st.markdown("""
    <style>
    .stApp {background-color: #121212; color: white;}
    .stMarkdown {color: white;}
    .stDataFrame {color: white;}
    </style>
    """, unsafe_allow_html=True)

# Favorites section in sidebar
st.sidebar.markdown("---")
st.sidebar.title("Your Favorites")

if not st.session_state.favorites:
    st.sidebar.write("You haven't added any favorites yet.")
else:
    for item in st.session_state.favorites:
        st.sidebar.write(f"- {item}")

# Get current page from session state
page = st.session_state.page

# Main content based on page selection
if page == "Home":
    st.header("Welcome to India's Cultural Journey")
    
    # Overview section
    st.subheader("Overview")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        India's cultural heritage spans thousands of years, encompassing diverse art forms, traditions, and historical sites.
        This application helps you explore:
        
        * **Traditional Art Forms** across different regions
        * **Cultural Tourism Trends** and seasonal patterns
        * **Government Initiatives** for preservation
        * **Responsible Tourism** opportunities
        """)
    
    with col2:
        # Map image
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/India-map-en.svg/800px-India-map-en.svg.png", caption="Map of India")
    
    st.markdown("---")
    st.subheader("Key Insights Preview")
    
    # Key insights metrics
    insight_col1, insight_col2, insight_col3 = st.columns(3)
    
    with insight_col1:
        st.metric(label="Traditional Art Forms Documented", value="100+")
    
    with insight_col2:
        st.metric(label="Annual Tourism Revenue", value="₹85,000 Cr")
    
    with insight_col3:
        st.metric(label="Cultural Sites Preserved", value="250+")

elif page == "Art Forms Explorer":
    st.header("Traditional Art Forms Explorer")
    
    if 'art' in data:
        # Sidebar filters
        st.sidebar.subheader("Filter Art Forms")
        art_types = ['All'] + sorted(data['art']['Type'].unique().tolist())
        selected_type = st.sidebar.selectbox("Art Type", art_types)
        
        regions = ['All'] + sorted(data['art']['Region'].unique().tolist())
        selected_region = st.sidebar.selectbox("Region", regions)
        
        # Filter data based on selections
        filtered_art = data['art']
        if selected_type != 'All':
            filtered_art = filtered_art[filtered_art['Type'] == selected_type]
        if selected_region != 'All':
            filtered_art = filtered_art[filtered_art['Region'] == selected_region]
        
        # Display art forms in two columns
        st.subheader("Explore Traditional Art Forms")
        
        # Map visualization
        st.subheader("Geographic Distribution of Art Forms")
        
        # Create a map centered on India
        m = create_folium_map()
        
        # Group art forms by region for the map
        region_art = data['art'].groupby('Region').agg({
            'Art_Form': 'count',
            'Cultural_Significance': 'mean'
        }).reset_index()
        
        # Add region information (this would need actual lat/long for regions)
        region_coords = {
            'Tamil Nadu': [11.1271, 78.6569],
            'Kerala': [10.8505, 76.2711],
            'North India': [28.7041, 77.1025],
            'Odisha': [20.9517, 85.0985],
            'Andhra Pradesh': [15.9129, 79.7400],
            'Manipur': [24.6637, 93.9063],
            'Assam': [26.2006, 92.9376],
            'Bihar': [25.0961, 85.3131],
            'Maharashtra': [19.7515, 75.7139],
            'Punjab': [31.1471, 75.3412],
            'Kashmir': [34.0837, 74.7973]
        }
        
        for idx, row in region_art.iterrows():
            if row['Region'] in region_coords:
                lat, lon = region_coords[row['Region']]
                popup_content = f"<b>{row['Region']}</b><br>Art Forms: {row['Art_Form']}<br>Significance: {row['Cultural_Significance']:.2f}"
                folium.Marker(
                    location=[lat, lon],
                    popup=popup_content,
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(m)
        
        # Display the map
        folium_static(m)
        
        # Display art forms in a table
        st.subheader("Art Forms List")
        st.dataframe(filtered_art[['Art_Form', 'Type', 'Region', 'Description', 'Cultural_Significance']])
        
        # Visualization of art forms by type
        st.subheader("Art Forms by Type")
        fig = px.pie(data['art'], names='Type', title='Distribution of Art Forms by Type')
        st.plotly_chart(fig, use_container_width=True)
        
        # Visualization of art forms by region
        st.subheader("Art Forms by Region")
        fig = px.bar(data['art'].groupby('Region').size().reset_index(name='count'), 
                    x='Region', y='count', title='Number of Art Forms by Region')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Art forms data not found. Please check the data processing step.")

elif page == "Cultural Tourism Analysis":
    st.header("Cultural Tourism Analysis")
    
    if 'tourism' in data and 'sites' in data:
        # Tourism trends over time
        st.subheader("Tourism Trends Over Time")
        fig = px.line(data['tourism'], x='Year', y=['Domestic_Visitors', 'International_Visitors'], 
                     title='Domestic vs International Tourism Trends')
        st.plotly_chart(fig, use_container_width=True)
        
        # Revenue analysis
        st.subheader("Tourism Revenue Analysis")
        fig = px.bar(data['tourism'], x='Year', y='Revenue_Crores', 
                    title='Annual Tourism Revenue (in Crores ₹)')
        st.plotly_chart(fig, use_container_width=True)
        
        # Cultural sites map
        st.subheader("Popular Cultural Sites")
        
        # Create a map for cultural sites
        sites_map = create_folium_map()
        
        # Add markers for cultural sites
        for idx, row in data['sites'].iterrows():
            popup_content = f"<b>{row['Site_Name']}</b><br>Type: {row['Type']}<br>Visitors: {row['Annual_Visitors']:,}<br>UNESCO: {'Yes' if row['UNESCO_Site'] else 'No'}"
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=popup_content,
                icon=folium.Icon(color='green' if row['UNESCO_Site'] else 'blue', icon='info-sign')
            ).add_to(sites_map)
        
        # Display the map
        folium_static(sites_map)
        
        # Top cultural sites by visitors
        st.subheader("Top Cultural Sites by Visitors")
        top_sites = data['sites'].sort_values('Annual_Visitors', ascending=False).head(10)
        fig = px.bar(top_sites, x='Site_Name', y='Annual_Visitors', 
                    title='Top 10 Cultural Sites by Annual Visitors')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Tourism or cultural sites data not found. Please check the data processing step.")

elif page == "Government Initiatives":
    st.header("Government Initiatives for Cultural Preservation")
    
    if 'funding' in data:
        # Funding trends over time
        st.subheader("Government Funding Trends")
        fig = px.line(data['funding'], x='Year', y='Amount_Crores', 
                     title='Government Funding for Cultural Preservation (in Crores ₹)')
        st.plotly_chart(fig, use_container_width=True)
        
        # Funding by category
        st.subheader("Funding by Category")
        funding_by_category = data['funding'].groupby('Category').sum().reset_index()
        fig = px.pie(funding_by_category, values='Amount_Crores', names='Category', 
                    title='Distribution of Funding by Category')
        st.plotly_chart(fig, use_container_width=True)
        
        # Funding by state
        st.subheader("Funding by State")
        funding_by_state = data['funding'].groupby('State').sum().reset_index()
        fig = px.bar(funding_by_state.sort_values('Amount_Crores', ascending=False), 
                    x='State', y='Amount_Crores', 
                    title='Government Funding by State')
        st.plotly_chart(fig, use_container_width=True)
        
        # Key initiatives
        st.subheader("Key Government Initiatives")
        initiatives = [
            {"name": "National Culture Fund", "description": "Public-private partnership for promoting Indian art and culture"},
            {"name": "Intangible Cultural Heritage Scheme", "description": "Documentation and preservation of intangible cultural heritage"},
            {"name": "Museum Grant Scheme", "description": "Financial assistance for setting up new museums"},
            {"name": "Cultural Function Grant Scheme", "description": "Support for organizing cultural events and festivals"},
            {"name": "Tagore Cultural Complexes", "description": "Multi-purpose cultural complexes across India"}
        ]
        
        for initiative in initiatives:
            st.markdown(f"**{initiative['name']}**: {initiative['description']}")
    else:
        st.error("Government funding data not found. Please check the data processing step.")

elif page == "Responsible Tourism":
    st.header("Responsible Tourism Recommendations")
    
    # Sustainable tourism practices
    st.subheader("Sustainable Tourism Practices")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### For Tourists
        * Respect local customs and traditions
        * Support local artisans and businesses
        * Minimize environmental impact
        * Learn basic phrases in local languages
        * Participate in community-based tourism
        """)
    
    with col2:
        st.markdown("""
        ### For Communities
        * Preserve authentic cultural experiences
        * Develop sustainable tourism infrastructure
        * Provide educational opportunities for visitors
        * Ensure fair distribution of tourism benefits
        * Maintain environmental conservation efforts
        """)
    
    # Case studies
    st.subheader("Successful Case Studies")
    case_studies = [
        {
            "title": "Kerala's Responsible Tourism Mission",
            "description": "Community-based tourism initiative that empowers local communities while providing authentic experiences for tourists."
        },
        {
            "title": "Sikkim's Eco-Tourism",
            "description": "Sustainable tourism model that balances environmental conservation with cultural preservation and economic development."
        },
        {
            "title": "Madhya Pradesh's Rural Tourism",
            "description": "Initiative to showcase rural art forms and traditions while creating livelihood opportunities for villagers."
        }
    ]
    
    for i, case in enumerate(case_studies):
        st.markdown(f"**{case['title']}**: {case['description']}")
    
    # Recommendations map
    st.subheader("Recommended Responsible Tourism Destinations")
    
    # Create a map for recommended destinations
    rec_map = create_folium_map()
    
    # Sample recommended destinations
    recommendations = [
        {"name": "Khonoma Green Village", "lat": 25.6573, "lon": 94.0244, "type": "Eco-Tourism"},
        {"name": "Hodka Artist Village", "lat": 23.3352, "lon": 69.6281, "type": "Cultural Tourism"},
        {"name": "Spiti Valley", "lat": 32.2464, "lon": 78.0349, "type": "Sustainable Tourism"},
        {"name": "Kumbalangi Model Village", "lat": 9.8723, "lon": 76.2711, "type": "Community Tourism"},
        {"name": "Majuli Island", "lat": 26.9452, "lon": 94.1780, "type": "Cultural Preservation"}
    ]
    
    # Add markers for recommended destinations
    for rec in recommendations:
        popup_content = f"<b>{rec['name']}</b><br>Type: {rec['type']}"
        folium.Marker(
            location=[rec['lat'], rec['lon']],
            popup=popup_content,
            icon=folium.Icon(color='green', icon='leaf')
        ).add_to(rec_map)
    
    # Display the map
    folium_static(rec_map)

# Add a feedback section at the bottom of the app
st.markdown("---")
st.subheader("Feedback & Suggestions")
col1, col2 = st.columns([3, 1])

with col1:
    feedback = st.text_area("Share your thoughts or suggestions for improvement:")
    email = st.text_input("Email (optional):")

with col2:
    st.write("")
    st.write("")
    if st.button("Submit Feedback"):
        if feedback:
            st.success("Thank you for your feedback!")
            # In a real app, you would save this feedback to a database
        else:
            st.error("Please enter some feedback before submitting.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center;'>
<p>Developed for YourStory Project | Data sourced from data.gov.in</p>
</div>
""", unsafe_allow_html=True)