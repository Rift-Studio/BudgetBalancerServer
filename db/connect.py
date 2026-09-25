import os
import psycopg2
from flask import Flask, g, jsonify
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# Database ---
# 1. Function to get or create a database connection for the current request
def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
    return g.db