from db.connect import get_db
from db.read_users import RETRIEVE_USER_ID
from security.password_manager import hash_new_password, verify_user_password

def getUserId(email: str, password: str):
    isError = False
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute(RETRIEVE_USER_ID, (email,))
        
        user = cursor.fetchall()
        isVerified = verify_user_password(user[0][1], password)  # Assuming the hash is the second column
        print("Logging in...")

        db.commit()
        print("Retrieved Id")
            
    except Exception as e:
        db.rollback()
        print(f"Error Logging in: {e}")
        isError = True
    finally:
        cursor.close()
        db.close()
    return user[0][0] if not isError and isVerified else "Failed to retrieve user id!"