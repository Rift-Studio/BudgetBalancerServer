import pandas as pd
import argparse
import os

# 1. Configuration
master_file = './data/prod_transactions.csv'

def update_transaction_category(tx_id: int, new_category: str):
    # Check if the master file exists
    if not os.path.exists(master_file):
        print(f"Error: The file '{master_file}' does not exist. Run the consolidation script first.")
        return

    # Load the dataset
    df = pd.read_csv(master_file)

    # Ensure the 'Category' column exists; if not, create it
    if 'Category' not in df.columns:
        df['Category'] = None

    # Check if the ID exists     in the dataset
    if tx_id not in df['ID'].values:
        print(f"Error: Transaction ID '{tx_id}' not found in the dataset.")
        return False

    # Update the Category for the matching ID row
    df.loc[df['ID'] == tx_id, 'Category'] = new_category

    # Save the updated data back to the CSV
    df.to_csv(master_file, index=False)
    print(f"Successfully updated transaction {tx_id} to Category: '{new_category}'")
    return True

# def begin_update_txn():
#     parser = argparse.ArgumentParser(description="Update the category of a specific transaction by its ID.")
    
#     # Require the ID and the new category string
#     parser.add_argument('--id', required=True, help="The unique ID of the transaction (e.g., TX-a1b2c3d4)")
#     parser.add_argument('--category', required=True, help="The new category name (e.g., Groceries, Business, Utilities)")

#     args = parser.parse_args()
    
#     # Run the update function
#     update_transaction_category(args.id, args.category)
