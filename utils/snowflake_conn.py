import snowflake.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_snowflake_connection():
    """
    Establishes and returns a connection to Snowflake.
    Requires environment variables to be set in a .env file.
    """
    try:
        conn = snowflake.connector.connect(
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
            database=os.getenv('SNOWFLAKE_DATABASE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA')
        )
        return conn
    except Exception as e:
        print(f"Error connecting to Snowflake: {e}")
        return None

def execute_query(query, params=None):
    """
    Executes a query on Snowflake and returns the results as a pandas DataFrame.
    
    Args:
        query (str): SQL query to execute
        params (dict, optional): Parameters for the query
        
    Returns:
        pandas.DataFrame: Results of the query
    """
    import pandas as pd
    
    conn = get_snowflake_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Fetch results and column names
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        
        # Create DataFrame
        df = pd.DataFrame(results, columns=column_names)
        return df
    except Exception as e:
        print(f"Error executing query: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

# Add this function to the existing snowflake_conn.py file

def upload_dataframe_to_snowflake(df, table_name, create_table=True):
    """
    Uploads a pandas DataFrame to a Snowflake table.
    
    Args:
        df (pandas.DataFrame): DataFrame to upload
        table_name (str): Name of the Snowflake table
        create_table (bool): Whether to create the table if it doesn't exist
        
    Returns:
        bool: True if successful, False otherwise
    """
    import pandas as pd
    
    conn = get_snowflake_connection()
    if conn is None:
        print("Failed to connect to Snowflake")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        if create_table:
            # Generate column definitions based on DataFrame dtypes
            columns = []
            for col, dtype in df.dtypes.items():
                if pd.api.types.is_integer_dtype(dtype):
                    col_type = "INTEGER"
                elif pd.api.types.is_float_dtype(dtype):
                    col_type = "FLOAT"
                elif pd.api.types.is_bool_dtype(dtype):
                    col_type = "BOOLEAN"
                else:
                    col_type = "VARCHAR(255)"
                columns.append(f'"{col}" {col_type}')
            
            # Create table
            create_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
            cursor.execute(create_query)
            print(f"Created table {table_name} in Snowflake")
        
        # Convert DataFrame to list of tuples for insertion
        values = [tuple(row) for row in df.values]
        placeholders = ", ".join(["(%s" + ", %s" * (len(df.columns) - 1) + ")"] * len(values))
        
        # Flatten the values list for cursor.execute
        flat_values = [item for sublist in values for item in sublist]
        
        # Insert data
        insert_query = f"INSERT INTO {table_name} ({', '.join([f'"{col}"' for col in df.columns])}) VALUES {placeholders}"
        cursor.execute(insert_query, flat_values)
        
        print(f"Successfully uploaded {len(df)} rows to {table_name}")
        return True
    except Exception as e:
        print(f"Error uploading data to Snowflake: {e}")
        return False
    finally:
        if conn:
            conn.close()