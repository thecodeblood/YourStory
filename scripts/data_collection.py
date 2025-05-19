import pandas as pd
import requests
import os
import json
from datetime import datetime

# Create data directories if they don't exist
os.makedirs('../data/raw', exist_ok=True)
os.makedirs('../data/processed', exist_ok=True)

def fetch_data_from_api(api_url, params=None):
    """
    Fetches data from an API endpoint.
    
    Args:
        api_url (str): URL of the API endpoint
        params (dict, optional): Query parameters for the API request
        
    Returns:
        dict: JSON response from the API
    """
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

def fetch_data_gov_in_datasets():
    """
    Fetches datasets related to art, culture, and tourism from data.gov.in.
    Saves the raw data to files in the data/raw directory.
    """
    # Base URL for data.gov.in API
    base_url = "https://api.data.gov.in/resource"
    
    # List of dataset IDs to fetch (these are examples and would need to be replaced with actual IDs)
    dataset_ids = [
        "tourism-statistics",
        "cultural-sites",
        "art-forms",
        "government-funding"
    ]
    
    # API key (would need to be obtained from data.gov.in)
    api_key = os.getenv("DATA_GOV_IN_API_KEY")
    
    if not api_key:
        print("Warning: DATA_GOV_IN_API_KEY environment variable not set.")
        print("You will need to register at data.gov.in to obtain an API key.")
        return
    
    for dataset_id in dataset_ids:
        print(f"Fetching dataset: {dataset_id}")
        
        # Construct API URL
        api_url = f"{base_url}/{dataset_id}"
        
        # Set up parameters
        params = {
            "api-key": api_key,
            "format": "json"
        }
        
        # Fetch data
        data = fetch_data_from_api(api_url, params)
        
        if data:
            # Save raw data to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"../data/raw/{dataset_id}_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            
            print(f"Saved raw data to {filename}")
        else:
            print(f"Failed to fetch data for {dataset_id}")

def download_sample_datasets():
    """
    Downloads sample datasets for development purposes.
    This function can be used when actual API access is not available.
    """
    # Sample URLs (these would need to be replaced with actual URLs)
    sample_datasets = {
        "tourism_statistics": "https://example.com/sample_tourism_data.csv",
        "cultural_sites": "https://example.com/sample_cultural_sites.csv",
        "art_forms": "https://example.com/sample_art_forms.csv",
        "government_funding": "https://example.com/sample_funding_data.csv"
    }
    
    for name, url in sample_datasets.items():
        try:
            print(f"Downloading sample dataset: {name}")
            df = pd.read_csv(url)
            
            # Save to CSV file
            filename = f"../data/raw/{name}_sample.csv"
            df.to_csv(filename, index=False)
            
            print(f"Saved sample data to {filename}")
        except Exception as e:
            print(f"Error downloading sample dataset {name}: {e}")

def create_mock_datasets():
    """
    Creates mock datasets for development when API access or sample datasets are not available.
    """
    print("Creating mock datasets for development...")
    
    # 1. Tourism Statistics Mock Data
    tourism_data = {
        "Year": list(range(2010, 2023)),
        "Domestic_Visitors": [45000000, 48000000, 52000000, 55000000, 59000000, 63000000, 68000000, 72000000, 76000000, 80000000, 74000000, 78000000, 85000000],
        "International_Visitors": [5000000, 5500000, 6000000, 6500000, 7000000, 7500000, 8000000, 8500000, 9000000, 9500000, 2500000, 3500000, 7000000],
        "Revenue_Crores": [50000, 55000, 60000, 65000, 70000, 75000, 80000, 85000, 90000, 95000, 40000, 60000, 85000]
    }
    tourism_df = pd.DataFrame(tourism_data)
    tourism_df.to_csv("../data/raw/tourism_statistics_mock.csv", index=False)
    
    # 2. Cultural Sites Mock Data
    sites = [
        "Taj Mahal", "Qutub Minar", "Red Fort", "Ajanta Caves", "Ellora Caves", 
        "Khajuraho Temples", "Hampi", "Mahabalipuram", "Konark Sun Temple", "Fatehpur Sikri",
        "Sanchi Stupa", "Meenakshi Temple", "Golden Temple", "Jaisalmer Fort", "Hawa Mahal"
    ]
    states = [
        "Uttar Pradesh", "Delhi", "Delhi", "Maharashtra", "Maharashtra", 
        "Madhya Pradesh", "Karnataka", "Tamil Nadu", "Odisha", "Uttar Pradesh",
        "Madhya Pradesh", "Tamil Nadu", "Punjab", "Rajasthan", "Rajasthan"
    ]
    visitors_2022 = [
        6500000, 3800000, 4200000, 1200000, 1500000, 
        950000, 1800000, 2200000, 1100000, 2800000,
        750000, 2500000, 3900000, 1700000, 2900000
    ]
    latitude = [
        27.1751, 28.5245, 28.6562, 20.5519, 20.0258, 
        24.8318, 15.3350, 12.6269, 19.8876, 27.0940,
        23.4795, 9.9252, 31.6200, 26.9157, 26.9239
    ]
    longitude = [
        78.0421, 77.1855, 77.2410, 75.7000, 75.1780, 
        79.9199, 76.4600, 80.1928, 86.0947, 77.6701,
        77.7388, 78.1198, 74.8765, 70.9083, 75.8267
    ]
    
    sites_data = {
        "Site_Name": sites,
        "State": states,
        "Visitors_2022": visitors_2022,
        "Latitude": latitude,
        "Longitude": longitude,
        "UNESCO_Heritage": [True, True, True, True, True, True, True, True, True, True, False, False, False, False, False]
    }
    sites_df = pd.DataFrame(sites_data)
    sites_df.to_csv("../data/raw/cultural_sites_mock.csv", index=False)
    
    # 3. Art Forms Mock Data
    art_forms = [
        "Bharatanatyam", "Kathakali", "Kathak", "Odissi", "Kuchipudi", 
        "Manipuri", "Mohiniyattam", "Sattriya", "Madhubani Painting", "Warli Painting",
        "Pattachitra", "Tanjore Painting", "Kalamkari", "Phulkari", "Pashmina"
    ]
    art_types = [
        "Dance", "Dance", "Dance", "Dance", "Dance", 
        "Dance", "Dance", "Dance", "Painting", "Painting",
        "Painting", "Painting", "Textile Art", "Embroidery", "Textile"
    ]
    regions = [
        "Tamil Nadu", "Kerala", "North India", "Odisha", "Andhra Pradesh", 
        "Manipur", "Kerala", "Assam", "Bihar", "Maharashtra",
        "Odisha", "Tamil Nadu", "Andhra Pradesh", "Punjab", "Kashmir"
    ]
    
    art_data = {
        "Art_Form": art_forms,
        "Type": art_types,
        "Region": regions,
        "Practitioners_Estimate": [15000, 8000, 20000, 12000, 9000, 5000, 4000, 3000, 7000, 6000, 5000, 8000, 10000, 12000, 15000],
        "Govt_Recognition": ["National", "National", "National", "National", "National", "National", "National", "National", "State", "State", "State", "State", "National", "State", "National"],
        "Tourism_Potential": ["High", "High", "High", "Medium", "Medium", "Medium", "Medium", "Low", "High", "Medium", "Medium", "High", "High", "Medium", "High"]
    }
    art_df = pd.DataFrame(art_data)
    art_df.to_csv("../data/raw/art_forms_mock.csv", index=False)
    
    # 4. Government Funding Mock Data
    years = list(range(2015, 2023))
    funding_data = {
        "Year": years * 3,
        "Ministry": ["Culture"] * 8 + ["Tourism"] * 8 + ["Textiles"] * 8,
        "Budget_Allocation_Crores": [
            2800, 3000, 2950, 3100, 3250, 3400, 2900, 3500,  # Culture
            1800, 1950, 2100, 2300, 2500, 2700, 1500, 2200,  # Tourism
            4500, 4700, 4900, 5100, 5300, 5500, 4800, 5700   # Textiles
        ],
        "Utilization_Percentage": [
            92, 94, 91, 95, 93, 90, 85, 88,  # Culture
            88, 90, 92, 94, 91, 89, 80, 85,  # Tourism
            95, 93, 96, 94, 97, 95, 90, 92   # Textiles
        ]
    }
    funding_df = pd.DataFrame(funding_data)
    funding_df.to_csv("../data/raw/government_funding_mock.csv", index=False)
    
    # 5. Seasonal Tourism Trends Mock Data
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    
    regions = ["North India", "South India", "East India", "West India", "Central India", "Northeast India"]
    
    # Create empty lists for each column
    month_col = []
    region_col = []
    visitors_col = []
    peak_season_col = []
    
    # Generate data for each region and month combination
    for region in regions:
        for month in months:
            month_col.append(month)
            region_col.append(region)
            
            # Assign visitor numbers based on region and month (simulating seasonal patterns)
            if region == "North India":
                if month in ["October", "November", "December", "January", "February"]:
                    visitors = np.random.randint(800000, 1200000)
                    peak = "Yes"
                else:
                    visitors = np.random.randint(300000, 700000)
                    peak = "No"
            elif region == "South India":
                if month in ["December", "January", "February", "March"]:
                    visitors = np.random.randint(900000, 1300000)
                    peak = "Yes"
                else:
                    visitors = np.random.randint(400000, 800000)
                    peak = "No"
            elif region == "East India":
                if month in ["October", "November", "December", "January"]:
                    visitors = np.random.randint(600000, 900000)
                    peak = "Yes"
                else:
                    visitors = np.random.randint(200000, 500000)
                    peak = "No"
            elif region == "West India":
                if month in ["November", "December", "January", "February"]:
                    visitors = np.random.randint(700000, 1100000)
                    peak = "Yes"
                else:
                    visitors = np.random.randint(300000, 600000)
                    peak = "No"
            elif region == "Central India":
                if month in ["October", "November", "February", "March"]:
                    visitors = np.random.randint(500000, 800000)
                    peak = "Yes"
                else:
                    visitors = np.random.randint(150000, 400000)
                    peak = "No"
            else:  # Northeast India
                if month in ["March", "April", "October", "November"]:
                    visitors = np.random.randint(300000, 600000)
                    peak = "Yes"
                else:
                    visitors = np.random.randint(100000, 250000)
                    peak = "No"
            
            visitors_col.append(visitors)
            peak_season_col.append(peak)
    
    seasonal_data = {
        "Month": month_col,
        "Region": region_col,
        "Visitors": visitors_col,
        "Peak_Season": peak_season_col
    }
    
    seasonal_df = pd.DataFrame(seasonal_data)
    seasonal_df.to_csv("../data/raw/seasonal_tourism_mock.csv", index=False)
    
    print("Mock datasets created successfully in the data/raw directory.")

# Add these imports at the top if not already present
import numpy as np
import os
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Update the main execution section at the bottom of the file
if __name__ == "__main__":
    # Create absolute paths for data directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    raw_data_dir = os.path.join(project_dir, "data", "raw")
    processed_data_dir = os.path.join(project_dir, "data", "processed")
    
    # Create directories with absolute paths
    os.makedirs(raw_data_dir, exist_ok=True)
    os.makedirs(processed_data_dir, exist_ok=True)
    
    # Try to fetch data from data.gov.in if API key is available
    if os.getenv("DATA_GOV_IN_API_KEY"):
        print("Using data.gov.in API key to fetch real data...")
        fetch_data_gov_in_datasets()
    else:
        # Otherwise create mock datasets for development
        print("No API key found. Creating mock datasets instead...")
        create_mock_datasets()
        
    print("Data collection complete!")