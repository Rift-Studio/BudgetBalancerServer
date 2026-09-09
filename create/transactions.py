import subprocess
import os
from flask import jsonify

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