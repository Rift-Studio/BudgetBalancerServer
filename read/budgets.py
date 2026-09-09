import csv
import os
from flask import jsonify

# Gets a local list of budgets and target budget amounts
def getBudgets():
    csv_file_path = os.path.join(os.path.dirname(__file__), '../parameters/budgets.csv')
    
    if not os.path.exists(csv_file_path):
        return jsonify({"status": "error", "message": "CSV file not found"}), 404
        
    try:
        rows_list = []
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                # Build the structure mapping from capitalized headers
                budget = {
                    "budget": str(row.get('Budget', '')),
                    "target": int(row.get('Target', 0.0))
                }
                rows_list.append(budget)
                
        return jsonify({"rows": rows_list})
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Gets a local list of category names for transaction category selections
def getCategories():
    txt_file_path = os.path.join(os.path.dirname(__file__), '../parameters/category_names.txt')
    
    if not os.path.exists(txt_file_path):
        return jsonify({"status": "error", "message": "CSV file not found"}), 404
        
    try:
        rows_list = []
        with open(txt_file_path, mode='r', encoding='utf-8') as file:
            rows_list = file.read().splitlines()
                
        return jsonify({"rows": rows_list})
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500