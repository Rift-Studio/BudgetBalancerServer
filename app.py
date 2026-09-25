from create.transactions import mergeUploadedTransactions
from create.users import createNewUser
from read.transactions import getTransactions
from read.budgets import getBudgets
from read.users import getUserId
from update.transactions import updateCategoryForTransaction, mergeNewTransactionsToMaster
from flask import Flask,g, request
from dotenv import load_dotenv
from test import test

# Load variables from the .env file
load_dotenv()

app = Flask(__name__)

# 2. Automatically close the database connection when the request finishes
@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()
# --- Database

@app.route('/')
def home():
    return "Hello! Your local Python server is running dynamically."

@app.route('/test', methods=['GET'])
def test_route():
    with app.app_context():
            return test()
    # return "Test function executed successfully."

# CREATE --- 
@app.route('/merge-txns', methods=['GET'])
def trigger_script():
    return mergeUploadedTransactions()
# --- CREATE

# READ ---
@app.route('/get-budgets', methods=['POST'])
def get_budgets():
    return getBudgets(request.form.get('user_id'))
    
@app.route('/get-txns', methods=['POST'])
def get_structured_csv():
    return getTransactions(request.form.get('user_id'))
# --- READ

# UPDATE ---
@app.route('/update-category', methods=['POST'])
def update_category_url_route():
    # Extract parameters from the URL query string
    transaction_id = request.args.get('id')
    new_category = request.args.get('newCategory')
    return updateCategoryForTransaction(request.form.get('user_id'), new_category, transaction_id)

@app.route('/append-new-transactions', methods=['GET'])
def update_transactions_with_new_csv():
    return mergeNewTransactionsToMaster()
# --- UPDATE

# Security ---
@app.route('/auth/login', methods=['POST'])
def login():
    return getUserId(request.form.get('email'), request.form.get('password'))

@app.route('/auth/create', methods=['POST'])
def create_user():
    return createNewUser(request.form.get('email'), request.form.get('password'))
# --- Security

# DESTROY ---
# --- DESTROY

# App.py Start
if __name__ == '__main__':
    app.run(debug=True, port=5000)
