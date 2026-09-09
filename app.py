from create.transactions import mergeUploadedTransactions
from read.transactions import getTransactions
from read.budgets import getBudgets, getCategories
from update.transactions import updateCategoryForTransaction, mergeNewTransactionsToMaster
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello! Your local Python server is running dynamically."

# CREATE --- 
@app.route('/merge-txns', methods=['GET'])
def trigger_script():
    return mergeUploadedTransactions()
# --- CREATE

# READ ---
@app.route('/get-budgets', methods=['GET'])
def get_budgets():
    return getBudgets()

@app.route('/get-categories', methods=['GET'])
def get_categories():
    return getCategories()
    
@app.route('/get-txns', methods=['GET'])
def get_structured_csv():
    return getTransactions()
# --- READ

# UPDATE ---
@app.route('/update-category', methods=['GET', 'POST'])
def update_category_url_route():
    # Extract parameters from the URL query string
    transaction_id = request.args.get('id')
    new_category = request.args.get('newCategory')
    return updateCategoryForTransaction(new_category,transaction_id)

@app.route('/append-new-transactions', methods=['GET'])
def update_transactions_with_new_csv():
    return mergeNewTransactionsToMaster()
# --- UPDATE

# DESTROY ---
# --- DESTROY

# App.py Start
if __name__ == '__main__':
    app.run(debug=True, port=5000)
