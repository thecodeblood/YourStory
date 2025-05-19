# Indian Cultural Heritage & Tourism Explorer
## Overview
This Streamlit application showcases India's rich cultural heritage and tourism opportunities through interactive visualizations, maps, and data-driven insights. The application provides a comprehensive exploration of traditional art forms, cultural sites, tourism statistics, and government initiatives for cultural preservation.

## Features
### Home
- Overview of India's cultural heritage
- Key insights preview with metrics on art forms, tourism revenue, and cultural sites
### Art Forms Explorer
- Interactive map showing geographic distribution of traditional art forms
- Filtering options by art type and region
- Visualizations of art forms by type and region
- Detailed information on practitioners, government recognition, and cultural significance
### Cultural Tourism Analysis
- Tourism trends over time (domestic vs. international visitors)
- Revenue analysis with annual tourism revenue charts
- Interactive map of popular cultural sites with UNESCO status indicators
- Seasonal tourism patterns and visitor demographics
### Government Initiatives
- Funding allocation for cultural preservation
- Year-over-year changes in cultural investment
- Impact assessment of government programs
### Responsible Tourism
- Guidelines for sustainable cultural tourism
- Community involvement initiatives
- Environmental impact considerations
## Data Sources
The application uses several datasets to provide comprehensive insights:

1. Art Forms Dataset ( art_forms_processed.csv )
   
   - Traditional Indian art forms with details on type, region, practitioners, and cultural significance
2. Cultural Sites Dataset ( cultural_sites_processed.csv )
   
   - Information on cultural and historical sites including visitor numbers, UNESCO status, and geographical coordinates
3. Tourism Statistics Dataset ( tourism_statistics_processed.csv )
   
   - Tourism trends data including visitor numbers, revenue, and seasonal patterns
4. Government Funding Dataset ( government_funding_processed.csv )
   
   - Data on government initiatives and funding for cultural preservation
5. Top Indian Places to Visit Dataset ( Top Indian Places to Visit.csv )
   
   - Comprehensive information about tourist destinations including ratings, entrance fees, and best times to visit
## Project Structure
```
.
├── app.py                  
# Main Streamlit application
├── assets/                 
# Static assets (images, 
etc.)
├── data/
│   ├── processed/          
# Processed datasets ready 
for visualization
│   └── raw/                
# Raw datasets (mock or from 
API)
├── scripts/
│   ├── data_collection.py  
# Scripts for collecting 
data from API or generating 
mock data
│   ├── data_processing.py  
# Data cleaning and 
transformation scripts
│   └── upload_to_snowflake.
py # Utility for uploading 
data to Snowflake
├── utils/
│   ├── snowflake_conn.py   
# Snowflake connection 
utilities
│   └── visualization.py    
# Visualization helper 
functions
└── requirements.txt        
# Project dependencies
```
## Setup and Installation
### Prerequisites
- Python 3.8 or higher
- Pip package manager
### Installation Steps
1. Clone the repository
2. Create and activate a virtual environment:
```
python -m venv venv
.\venv\Scripts\activate
```
3. Install the required packages:
```
pip install -r requirements.
txt
```
4. Run the data collection script to generate or fetch data:
```
python 
scripts\data_collection.py
```
5. Process the raw data:
```
python 
scripts\data_processing.py
```
6. (Optional) Upload the processed data to Snowflake:
```
python 
scripts\upload_to_snowflake.
py
```
7. Run the Streamlit application:
```
streamlit run app.py
```
## Data Collection Options
The application supports multiple data sources:

1. API Data : If you have a DATA_GOV_IN_API_KEY environment variable set, the application will attempt to fetch real data from data.gov.in
2. Mock Data : If no API key is available, the application will generate mock datasets for development and testing
3. External CSV Files : You can also import your own CSV datasets by placing them in the appropriate directory
## Customization
The application includes a customization sidebar where users can:

- Switch between light and dark themes
- Save favorite art forms or cultural sites
- Provide feedback on the application
## Contributing
Contributions to enhance the application are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Data.gov.in for providing access to cultural datasets
- Streamlit for the interactive web application framework
- Plotly and Folium for the visualization libraries