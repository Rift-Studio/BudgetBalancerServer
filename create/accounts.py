from db.connect import get_db
from db.create_acct import CREATE_ACCT

def createAccounts(user_id: str,name: str, entity: str, accType: str, balance: float = 0.0):
    try:
        db = get_db()
        cursor = db.cursor()
        # Step 1: Create a temporary table matching the CSV structure (without user_id)
        
        # Step 3: Insert data from staging into the real table, adding user_id
        cursor.execute(CREATE_ACCT, (name, entity, accType, balance, user_id))
        print("Account data successfully loaded into real table!")

        db.commit()
        print("Account data successfully imported with user_id!")
            
    except Exception as e:
        db.rollback()
        print(f"Error adding account data: {e}")
    finally:
        cursor.close()
        db.close()
