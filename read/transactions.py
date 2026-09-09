import csv
import os
from flask import jsonify

#  Get the master list of transactions
def getTransactions():
    csv_file_path = os.path.join(os.path.dirname(__file__), '../data/prod_transactions.csv')
    
    if not os.path.exists(csv_file_path):
        return jsonify({"status": "error", "message": "CSV file not found"}), 404
        
    try:
        rows_list = []
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                # Convert the capitalized AMOUNT header to a float safely
                try:
                    amount_val = float(row.get('Amount', 0.0))
                except (ValueError, TypeError):
                    amount_val = 0.0  # Fallback if data is corrupted or missing

                # Build the structure mapping from capitalized headers
                transaction = {
                    "id": str(row.get('ID', '')),
                    "date": str(row.get('Date', '')),
                    "description": str(row.get('Description', '')),
                    "originalDescription": str(row.get('Original_Description', '')),
                    "amount": amount_val,
                    "type": str(row.get('Type','')),
                    "category": str(row.get('Category', '')),
                    "parentCategory": str(row.get('parentCategory', '')),
                    "originalCategory": str(row.get('Original_Category','')),
                    "account": str(row.get('Account', '')),
                    # "tags": str(row.get("Tags")),
                    "memo": str(row.get("Memo",'')),
                    "pending": bool(row.get("Pending",''))
                }
                rows_list.append(transaction)
                
        return jsonify({"rows": rows_list})
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500