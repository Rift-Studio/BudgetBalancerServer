CREATE_ACCT = """
INSERT INTO accounts (name, entity, type, balance, user_id)
VALUES (%s, %s, %s, %s, %s);
"""