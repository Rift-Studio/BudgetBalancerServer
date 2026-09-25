import subprocess
import os
from db.connect import get_db
from db.create_txns import COPY_STAGING_TRANSACTIONS, CREATE_TEMP_TABLE, INSERT_TRANSACTIONS_WITH_USER_ID
from flask import jsonify

def submitTransactionsToDB():
    try:
        db = get_db()
        cursor = db.cursor()
        user_id_to_add = "59cd092c-f7d4-47ec-a349-3db8aa67264b"  # The user_id value you want to append
        # Step 1: Create a temporary table matching the CSV structure (without user_id)
        cursor.execute(CREATE_TEMP_TABLE)
        csv_path = os.path.join(os.path.dirname(__file__), '../outputs/master_transactions.csv')

        # Step 2: Use copy_expert to load the CSV file into the staging table
        with open(csv_path, 'r', encoding='utf-8') as f:
            cursor.copy_expert(
               COPY_STAGING_TRANSACTIONS,
                f
            )
        print("CSV data successfully loaded into staging table!")

        # Step 3: Insert data from staging into the real table, adding user_id
        cursor.execute(INSERT_TRANSACTIONS_WITH_USER_ID, (user_id_to_add,))
        print("CSV data successfully loaded into real table!")

        db.commit()
        print("CSV data successfully imported with user_id!")

    except Exception as e:
        db.rollback()
        print(f"Error importing CSV: {e}")
    finally:
        cursor.close()
        db.close()

# Merge the Locally stored csv files under the statements folder, all csv will be merged to master list in /outputs
def mergeUploadedTransactions():
    try:
        # Find the path to the script in the same directory
        script_path = os.path.join(os.path.dirname(__file__), 'transaction-merger.py')
        
        # Run the script and capture what it prints
        result = subprocess.run(
            ['python', script_path, '--csvFolder', '../statements', '--outputFile', '../outputs/master-transactions.csv'], 
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