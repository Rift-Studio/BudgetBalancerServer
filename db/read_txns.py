GET_USER_TRANSACTIONS = """
        SELECT * 
        FROM transactions
        where user_id = %(user_id)s;
"""