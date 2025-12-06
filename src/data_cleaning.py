import pandas as pd
import numpy as np

def clean_sales_data(input_file='sales_data_raw (1).csv', output_file='sales_data_clean.csv'):
    """
    Clean sales data by handling duplicates, missing values, and inconsistencies.
    """
    # Read the CSV file
    df = pd.read_csv(input_file, skipinitialspace=True)
    
    # Clean column names - strip whitespace
    df.columns = df.columns.str.strip()
    
    # Clean ProdName: strip whitespace and convert to title case
    df['ProdName'] = df['ProdName'].str.strip().str.title()
    
    # Clean CATEGORY: strip whitespace, remove quotes, convert to title case
    df['CATEGORY'] = df['CATEGORY'].str.strip().str.replace('"', '').str.strip().str.title()
    
    # Clean Price: ensure numeric, replace 0 with NaN
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df.loc[df['Price'] == 0, 'Price'] = np.nan
    
    # Clean qty: handle negative values and missing data
    df['qty'] = pd.to_numeric(df['qty'], errors='coerce')
    df.loc[df['qty'] < 0, 'qty'] = np.nan
    df.loc[df['qty'] == 0, 'qty'] = np.nan
    
    # Clean date_sold: standardize date format
    df['date_sold'] = pd.to_datetime(df['date_sold'], errors='coerce')
    
    # Fill missing values by grouping similar products
    for col in ['Price', 'qty', 'date_sold']:
        if col in df.columns:
            df[col] = df.groupby(['ProdName', 'CATEGORY'])[col].transform(
                lambda x: x.fillna(x.mode()[0] if not x.mode().empty else x.mean())
            )
    
    # Remove duplicate rows
    df = df.drop_duplicates(subset=['ProdName', 'CATEGORY', 'Price', 'qty', 'date_sold'], keep='first')
    
    # Sort by date
    df = df.sort_values('date_sold').reset_index(drop=True)
    
    # Save cleaned data
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")
    print(f"Original rows: {pd.read_csv(input_file).shape[0]}, Cleaned rows: {df.shape[0]}")
    
    return df

if __name__ == "__main__":
    clean_sales_data()