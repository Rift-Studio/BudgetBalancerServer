import email
import subprocess
import os
from db.connect import get_db
from db.update_txns import UPDATE_TRANSACTION_CATEGORY
from scripts.update import update_transaction_category
from flask import jsonify

# add transactions found in new cvs that don't exist in current master beyond the latest date
def mergeNewTransactionsToMaster():
    try:
        # Find the path to the script in the same directory
        # script_path = os.path.join(os.path.dirname(__file__), './scripts/transaction-appender.py')
        script_path = './scripts/transaction-appender.py'


        # Run the script and capture what it prints
        result = subprocess.run(
            ['python', script_path], 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        # Return the script's output to the browser
        return jsonify({
            "status": "success",
            "output": result.stdout.strip()
        })
        
    except subprocess.CalledProcessError as e:
        # Return errors if the script crashes
        return jsonify({
            "status": "error",
            "message": e.stderr.strip()
        }), 500

# Locally save a new category for a specific transaction
def updateCategoryForTransaction(user_id, new_category, transaction_id):
    
    # Validate that both parameters were provided
    if not transaction_id or not new_category or not user_id:
        return jsonify({
            "status": "error", 
            "message": "All parameters are required"
        }), 400

    try:
        db = get_db()
        cursor = db.cursor()
        print(f"Updating transaction {transaction_id} for user {user_id} to new category: {new_category}")
        cursor.execute(UPDATE_TRANSACTION_CATEGORY, {
            "new_category": str(new_category),
            "user_id": str(user_id),
            "transaction_id": str(transaction_id)
        })
        db.commit()
    except Exception as e:
            db.rollback()
            print(f"Error importing CSV: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500
    finally:
            cursor.close()
            db.close()
            return jsonify({"status": "success", "message": "Transaction updated successfully"}), 200

        
