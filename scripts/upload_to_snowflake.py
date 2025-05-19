import pandas as pd
import os
import sys

# Add parent directory to path to import utils
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.append(project_dir)

from utils.snowflake_conn import upload_dataframe_to_snowflake

def upload_all_processed_data():
    """Upload all processed datasets to Snowflake"""
    # Get paths
    processed_dir = os.path.join(project_dir, 'data', 'processed')
    
    # List of datasets to upload
    datasets = [
        {'file': 'tourism_statistics_processed.csv', 'table': 'TOURISM_STATISTICS'},
        {'file': 'cultural_sites_processed.csv', 'table': 'CULTURAL_SITES'},
        {'file': 'art_forms_processed.csv', 'table': 'ART_FORMS'},
        {'file': 'government_funding_processed.csv', 'table': 'GOVERNMENT_FUNDING'}
    ]
    
    for dataset in datasets:
        file_path = os.path.join(processed_dir, dataset['file'])
        if os.path.exists(file_path):
            print(f"Uploading {dataset['file']} to Snowflake table {dataset['table']}...")
            df = pd.read_csv(file_path)
            upload_dataframe_to_snowflake(df, dataset['table'])
        else:
            print(f"File not found: {file_path}")

if __name__ == "__main__":
    upload_all_processed_data()
    print("Data upload to Snowflake complete!")