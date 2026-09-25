from flask import jsonify
from db.connect import get_db
import db.read_budg as read_budg

# Gets a local list of budgets and target budget amounts
def getBudgets(user_id: str):
    #  Get the master list of budgets
    try:
        # Get the database connection and create a cursor
        db = get_db()
        cursor = db.cursor()
        
        print(f"attempting budgets with: {user_id}")

        # Execute your SQL query
        cursor.execute(read_budg.RETRIEVE_BUDGETS, (user_id,))
        print(f"Executed query to fetch budgets for user_id: {user_id}")
        budgets = cursor.fetchall()
        print(f"Fetched {len(budgets)} budgets from the database.")
        print("Budgets data:", budgets)  # Print the fetched budgets for debugging
        rows_list = []

        # 
        for row in budgets:
            # Convert the capitalized AMOUNT header to a float safely
            try:
                amount_val = int(row[2])
            except (ValueError, TypeError):
                amount_val = 0  # Fallback if data is corrupted or missing

            budget = {
                "id": str(row[0]),
                "name": str(row[1]),
                "target": amount_val,
                "type": str(row[3]),
            }
            rows_list.append(budget)
                        
        # 
        cursor.close()
        return jsonify({"rows": rows_list})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500