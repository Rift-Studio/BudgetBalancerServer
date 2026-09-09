import pandas as pd
import glob
import os
import uuid  # NEW: Imported for unique ID generation
import argparse
from pathlib import Path

# 1. Initialize the argument parser
parser = argparse.ArgumentParser(description="A sample script that processes arguments.")

# 2. Define expected arguments
# --user: A required string argument
parser.add_argument("--csvFolder", type=str, default= './statements', help="Location of csv files")
    
# --age: An optional integer argument with a default value
parser.add_argument("--outputFile", type=str, default='./outputs/master_transactions.csv', help="Path of output master csv file")

# 3. Parse the incoming command-line arguments
args = parser.parse_args()

# 1. Configuration
csv_folder = args.csvFolder  # Folder where your CSV files are located
output_file = args.outputFile

# Define your unified master schema
# Map your various source headers (values) to the standard column name (key)
column_mappings = {
    'Date': ['date', 'Date', 'Transaction Date'],
    'Description': ['description', 'Description', 'Desc', 'memo', 'Details'],
    'Original_Description': ['Original Description'],
    'Amount': ['amount', 'Amount', 'Total', 'Transaction Amount', 'Amount-Combined'],
    'Type': ['Type'], #Credit/Debit,
    'Parent_Category': ['Parent Category'],
    # 'Category': ['Category'],
    'Original_Category': ['Category'],
    'Account': ['Account'],
    # 'Tags': ['Tags'],
    'Memo': ['Memo'],
    'Pending': ['Pending']
}

# 2. Function to standardize and clean data
def standardize_dataframe(file_path):
    df = pd.read_csv(file_path)
    new_df = pd.DataFrame()
    if 'Debit' in df.columns: #applies to citi card only, change to if num exists in that column then change the type column value to the debit or credit string
        if 'Credit' in df.columns:
            df['Amount-Combined'] = df['Debit'].combine_first(df['Credit'])

    # Map existing columns to the unified schema
    for standard_col, possible_names in column_mappings.items():
        found = False
        for col in possible_names:
            if col in df.columns:
                new_df[standard_col] = df[col]
                found = True
                break
        # If no matching column is found, fill with empty values
        if not found:
            new_df[standard_col] = None 
            
    # Optional: Add the source filename to track origins
    new_df['Category'] = 'Unknown'
    # new_df['Account'] = Path(file_path).stem
    
    return new_df

# Helper function to find the first word with at least 3 characters
def get_first_long_word(text):
    words = text.split()
    # Generator expression returns the first word matching the length constraint
    return next((word for word in words if len(word) >= 3), '')

# 3. Combine all CSV files
all_files = glob.glob(os.path.join(csv_folder, "*.csv"))
dataframes = []

for filename in all_files:
    df = standardize_dataframe(filename)
    dataframes.append(df)

# Concatenate into a single master dataset
if dataframes:
    master_df = pd.concat(dataframes, ignore_index=True)
    
    # --- NEW: DATE STANDARDIZATION & SORTING ---
    # Automatically parse mixed date formats (e.g., 2026-07-17, 07/17/2026, 17-Jul-2026)
    master_df['Date'] = pd.to_datetime(master_df['Date'], errors='coerce', format='mixed')
    
    # Sort chronologically (oldest to newest)
    master_df = master_df.sort_values(by='Date', ascending=True)
    
    # Reformat the date column strictly to MM/DD/YYYY
    master_df['Date'] = master_df['Date'].dt.strftime('%m/%d/%Y')
    # --------------------------------------------

    # --- NEW: UNIQUE ID GENERATION ---
    # Generate a unique ID for each transaction (e.g., '7b2c8a91')
    # master_df['ID'] = [f"{uuid.uuid4().hex[:8]}" for _ in range(len(master_df))]
    master_df['ID'] = range(1, len(master_df) + 1)
    
    # Move the ID column to the front of the file for better readability
    cols = ['ID'] + [col for col in master_df.columns if col != 'ID']
    master_df = master_df[cols]
    # ----------------------------------

    # Optional: Clean the master data (e.g., remove currency symbols, handle NaNs)
    master_df['Amount'] = master_df['Amount'].astype(str).str.replace('$', '', regex=False)
    # master_df['Short_Description'] = (
    #     master_df['Description']
    #     .astype(str)
    #     .str.replace(r'\bthe\b', '', case=False, regex=True) # 1. Remove "the"
    #     .str.replace(r'\.com\b', '', case=False, regex=True) # 1. Remove ".com"
    #     .str.replace(r'\s+', ' ', regex=True)
    #     .str.replace(r'[^a-zA-Z\s-]', '', regex=True)         # 2. Keep only letters and spaces 
    #     .str.upper()                                         # 3. Convert all text to UPPERCASE
    #     .apply(get_first_long_word)                          # 4. Extract the first word >= 3 characters
    # )
    # master_df['Description'] = (
    #     master_df['Description']
    #     .astype(str)
    #     .str.replace(r'\d+', ' ', regex=True)
    #     .str.replace(r'\bthe\b', '', case=False, regex=True) # 1. Remove "the"
    #     .str.replace(r'\.com\b', '', case=False, regex=True) # 1. Remove ".com"
    #     .str.replace(r'\s+', ' ', regex=True)
    #     .str.replace(r'[^a-zA-Z\s]', '', regex=True)         # 2. Keep only letters and spaces 
    #     .str.lower()                                         # 3. Convert all text to Lowercase
    # )

    # master_df['Description'] = master_df['Description'].astype(str).str.replace(r'\s.*', '', regex=True)
    # master_df['Description'] = master_df['Description'].astype(str).str.replace(r'\s+', ' ', regex=True)

    # Save to a new CSV file
    master_df.to_csv(output_file, index=False)
    print(f"Successfully consolidated {len(dataframes)} files into {output_file}")
else:
    print(f"No CSV files found in the specified folder. {csv_folder}")
