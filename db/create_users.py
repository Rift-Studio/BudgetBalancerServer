CREATE_NEW_USER = """
    INSERT INTO users (email, password_hash)
    VALUES (%s, %s)
"""