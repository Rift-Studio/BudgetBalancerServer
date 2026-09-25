RETRIEVE_BUDGETS = """
SELECT * FROM budgets WHERE user_id = %s;
"""