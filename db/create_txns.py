COPY_TRANSACTIONS_CSV = """
    COPY transactions ({columns}, user_id) 
    FROM STDIN 
    WITH CSV HEADER;
"""

CREATE_TEMP_TABLE = """
    CREATE TEMP TABLE staging_transactions (
        date DATE,
        description VARCHAR,
        original_description VARCHAR,
        amount FLOAT,
        type VARCHAR,
        parent_category VARCHAR,
        original_category VARCHAR,
        account VARCHAR,
        memo VARCHAR,
        pending BOOL,
        category VARCHAR
    ) ON COMMIT DROP;
"""

COPY_STAGING_TRANSACTIONS = """
    COPY staging_transactions FROM STDIN WITH CSV HEADER
"""

INSERT_TRANSACTIONS_WITH_USER_ID = """
    INSERT INTO transactions (date, description, original_description, amount, type, parent_category, original_category, account, memo, pending, category, user_id)
    SELECT date, description, original_description, amount, type, parent_category, original_category, account, memo, pending, category, %s
    FROM staging_transactions
    ON CONFLICT (id) DO NOTHING;
"""