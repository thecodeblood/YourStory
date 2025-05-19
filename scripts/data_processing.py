import pandas as pd
import os
import json
import glob

def process_tourism_statistics(input_file, output_file):
    """Process tourism statistics data"""
    df = pd.read_csv(input_file)
    
    # Data cleaning and transformation
    # 1. Handle missing values
    df = df.fillna(0)
    
    # 2. Add calculated columns
    df['Total_Visitors'] = df['Domestic_Visitors'] + df['International_Visitors']
    df['International_Percentage'] = (df['International_Visitors'] / df['Total_Visitors'] * 100).round(2)
    
    # 3. Save processed data
    df.to_csv(output_file, index=False)
    print(f"Processed tourism statistics saved to {output_file}")
    return df

def process_cultural_sites(input_file, output_file):
    """Process cultural sites data"""
    df = pd.read_csv(input_file)
    
    # Data cleaning and transformation
    # 1. Add region classification based on state
    north_states = ['Jammu and Kashmir', 'Himachal Pradesh', 'Punjab', 'Uttarakhand', 'Haryana', 'Delhi', 'Uttar Pradesh']
    south_states = ['Karnataka', 'Andhra Pradesh', 'Tamil Nadu', 'Kerala', 'Telangana']
    east_states = ['Bihar', 'Jharkhand', 'West Bengal', 'Odisha']
    west_states = ['Rajasthan', 'Gujarat', 'Maharashtra', 'Goa']
    central_states = ['Madhya Pradesh', 'Chhattisgarh']
    northeast_states = ['Sikkim', 'Assam', 'Meghalaya', 'Tripura', 'Mizoram', 'Manipur', 'Nagaland', 'Arunachal Pradesh']
    
    def get_region(state):
        if state in north_states:
            return 'North India'
        elif state in south_states:
            return 'South India'
        elif state in east_states:
            return 'East India'
        elif state in west_states:
            return 'West India'
        elif state in central_states:
            return 'Central India'
        elif state in northeast_states:
            return 'Northeast India'
        else:
            return 'Other'
    
    df['Region'] = df['State'].apply(get_region)
    
    # 2. Categorize sites by visitor volume
    df['Popularity'] = pd.cut(
        df['Visitors_2022'], 
        bins=[0, 1000000, 3000000, float('inf')],
        labels=['Low', 'Medium', 'High']
    )
    
    # 3. Save processed data
    df.to_csv(output_file, index=False)
    print(f"Processed cultural sites data saved to {output_file}")
    return df

def process_art_forms(input_file, output_file):
    """Process art forms data"""
    df = pd.read_csv(input_file)
    
    # Data cleaning and transformation
    # 1. Create a tourism potential score (numeric)
    potential_map = {'Low': 1, 'Medium': 2, 'High': 3}
    df['Tourism_Potential_Score'] = df['Tourism_Potential'].map(potential_map)
    
    # 2. Create recognition level score
    recognition_map = {'State': 1, 'National': 2, 'International': 3}
    df['Recognition_Score'] = df['Govt_Recognition'].map(recognition_map)
    
    # 3. Calculate overall cultural significance score
    df['Cultural_Significance'] = (df['Tourism_Potential_Score'] + df['Recognition_Score']) / 2
    
    # 4. Save processed data
    df.to_csv(output_file, index=False)
    print(f"Processed art forms data saved to {output_file}")
    return df

def process_government_funding(input_file, output_file):
    """Process government funding data"""
    df = pd.read_csv(input_file)
    
    # Data cleaning and transformation
    # 1. Calculate actual utilization
    df['Actual_Utilization_Crores'] = (df['Budget_Allocation_Crores'] * df['Utilization_Percentage'] / 100).round(2)
    
    # 2. Calculate year-over-year growth
    df = df.sort_values(['Ministry', 'Year'])
    df['YoY_Budget_Growth'] = df.groupby('Ministry')['Budget_Allocation_Crores'].pct_change() * 100
    df['YoY_Budget_Growth'] = df['YoY_Budget_Growth'].round(2)
    
    # 3. Save processed data
    df.to_csv(output_file, index=False)
    print(f"Processed government funding data saved to {output_file}")
    return df

def process_all_datasets():
    """Process all datasets in the raw data directory"""
    # Get script directory and construct paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    raw_dir = os.path.join(project_dir, 'data', 'raw')
    processed_dir = os.path.join(project_dir, 'data', 'processed')
    
    # Ensure processed directory exists
    os.makedirs(processed_dir, exist_ok=True)
    
    # Process tourism statistics
    tourism_files = glob.glob(os.path.join(raw_dir, '*tourism_statistics*.csv'))
    if tourism_files:
        process_tourism_statistics(
            tourism_files[0], 
            os.path.join(processed_dir, 'tourism_statistics_processed.csv')
        )
    
    # Process cultural sites
    sites_files = glob.glob(os.path.join(raw_dir, '*cultural_sites*.csv'))
    if sites_files:
        process_cultural_sites(
            sites_files[0], 
            os.path.join(processed_dir, 'cultural_sites_processed.csv')
        )
    
    # Process art forms
    art_files = glob.glob(os.path.join(raw_dir, '*art_forms*.csv'))
    if art_files:
        process_art_forms(
            art_files[0], 
            os.path.join(processed_dir, 'art_forms_processed.csv')
        )
    
    # Process government funding
    funding_files = glob.glob(os.path.join(raw_dir, '*government_funding*.csv'))
    if funding_files:
        process_government_funding(
            funding_files[0], 
            os.path.join(processed_dir, 'government_funding_processed.csv')
        )

if __name__ == "__main__":
    process_all_datasets()
    print("Data processing complete!")