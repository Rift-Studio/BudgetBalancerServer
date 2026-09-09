import pandas as pd
import glob
import os
import uuid  # NEW: Imported for unique ID generation
import sys
import subprocess
from pathlib import Path

#  Paths are relative to the executable python script, not this file location. so everything is running from wherever the script is ran from
# may be problematic for server

# 1. Configuration
csv_folder = './statements'  # Folder where your CSV files are located
output_file = './scripts/temp/temp_master_transactions.csv'

def makeTemporaryTransactionsList():
    # Define the script name and the arguments as separate list items
    script_name = "./scripts/transaction-merger.py"

    # Build the command array
    command = [
        sys.executable,  # Automatically uses the path to your current Python interpreter
        script_name,
        "--csvFolder", csv_folder,
        "--outputFile", output_file
    ]

    print(f"Launching {script_name} from launcher.py...")
    
    # Execute the script and wait for it to finish
    subprocess.run(command)
    # Merge the new list with the main list
    subprocess.run([
        sys.executable, './scripts/csvMerger.py'
    ])

# Start
makeTemporaryTransactionsList()