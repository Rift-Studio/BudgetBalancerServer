import sys
import subprocess

#  Paths are relative to the executable python script, not this file location. so everything is running from wherever the script is ran from
# may be problematic for server

# 1. Configuration
csv_folder = './statements'  # Folder where your CSV files are located
output_file = './outputs/master_transactions.csv'

def mergeCsv():
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