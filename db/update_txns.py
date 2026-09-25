UPDATE_TRANSACTION_CATEGORY = """
    UPDATE transactions
    SET category = %(new_category)s
    WHERE user_id = %(user_id)s and id = %(transaction_id)s;
"""