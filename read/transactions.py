from flask import jsonify
from db.connect import get_db
import db.read_txns as read_txns

#  Get the master list of transactions
def getTransactions(user_id: str):
    try:
        # Get the database connection and create a cursor
        db = get_db()
        cursor = db.cursor()
        
        # Execute your SQL query
        cursor.execute(read_txns.GET_USER_TRANSACTIONS, {'user_id': user_id})
        transactions = cursor.fetchall()
        rows_list = []

        # 
        for row in transactions:
            # Convert the capitalized AMOUNT header to a float safely
            try:
                amount_val = float(row[7])
            except (ValueError, TypeError):
                amount_val = 0.0  # Fallback if data is corrupted or missing

            transaction = {
                "id": str(row[0]),
                "date": str(row[1]),
                "description": str(row[2]),
                "originalDescription": str(row[3]),
                "category": str(row[4]),
                "parentCategory": str(row[5]),
                "originalCategory": str(row[6]),
                "amount": amount_val,
                "type": str(row[8]),
                "account": str(row[9]),
                # "tags": str(row[0]),
                "memo": str(row[10]),
                "pending": bool(row[11]),
            }
            rows_list.append(transaction)
                              
        # 
        rows_list.sort(key=lambda x: x['date'], reverse=False)  # Sort by date in descending order
        cursor.close()
        return jsonify({"rows": rows_list})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500