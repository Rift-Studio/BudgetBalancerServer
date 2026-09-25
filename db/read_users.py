RETRIEVE_USER_ID = """
    SELECT id, password_hash
    FROM users
    WHERE email = %s
"""