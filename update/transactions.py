import subprocess
import os
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
def updateCategoryForTransaction(new_category, transaction_id):
    
    # Validate that both parameters were provided
    if not transaction_id or not new_category:
        return jsonify({
            "status": "error", 
            "message": "Both 'id' and 'newCategory' parameters are required"
        }), 400

    try:
        # Cast parameters explicitly to String and call your function
        success = update_transaction_category(int(transaction_id), str(new_category))
        
        if success:
            return jsonify({
                "status": "success", 
                "message": f"Transaction {transaction_id} updated to {new_category}"
            })
        else:
            return jsonify({"status": "error", "message": "Transaction ID not found"}), 404
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
