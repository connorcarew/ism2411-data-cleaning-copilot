import pandas as pd
import os

def load_data(file_path: str):
    """Load data from a CSV file."""
    df = pd.read_csv(file_path)
    return df


def clean_column_names(df):
    """Clean column names by converting to lowercase and replacing spaces with underscores."""
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    return df


def clean_data(df):
    """Clean the data by removing duplicates and handling missing values."""
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Remove rows with missing values
    df = df.dropna()
    
    return df


def save_data(df, output_path: str):
    """Save cleaned data to a CSV file."""
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")


if __name__ == "__main__":
    # Define file paths
    raw_data_path = "data/raw/sales_data_raw.csv"
    processed_data_path = "data/processed/sales_data_clean.csv"
    
    # Load data
    df = load_data(raw_data_path)
    print(f"Loaded {len(df)} rows from {raw_data_path}")
    
    # Clean column names
    df = clean_column_names(df)
    print("Column names cleaned")
    
    # Clean data
    df = clean_data(df)
    print(f"Data cleaned. {len(df)} rows remaining")
    
    # Save cleaned data
    save_data(df, processed_data_path)