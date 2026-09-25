from flask import jsonify
from db.connect import get_db
import db.read_txns as read_txns

#  Get the master list of accounts
def getAccounts(user_id: str):
    try:
        # Get the database connection and create a cursor
        db = get_db()
        cursor = db.cursor()
        
        # Execute your SQL query
        cursor.execute(read_txns.RETRIEVE_ACCOUNTS, (user_id,))
        print(f"Executed query to fetch accounts for user_id: {user_id}")
        accounts = cursor.fetchall()
        print(f"Fetched {len(accounts)} accounts from the database.")
        print("Accounts data:", accounts)  # Print the fetched accounts for debugging
        rows_list = []

        # 
        for row in accounts:
            # Convert the capitalized AMOUNT header to a float safely
            try:
                amount_val = float(row[3])
            except (ValueError, TypeError):
                amount_val = 0.0  # Fallback if data is corrupted or missing

            acct = {
                "id": str(row[0]),
                "name": str(row[1]),
                "entity": str(row[2]),
                "type": str(row[3]),
                "balance": amount_val,
            }
            rows_list.append(acct)
                        
        # 
        cursor.close()
        return jsonify({"rows": rows_list})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500