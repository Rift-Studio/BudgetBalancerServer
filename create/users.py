from db.connect import get_db
from db.create_users import CREATE_NEW_USER
from security.password_manager import hash_new_password

def createNewUser(email: str, password: str):
    isError = False
    try:
        db = get_db()
        cursor = db.cursor()
        hashed_password = hash_new_password(password)
        cursor.execute(CREATE_NEW_USER, (email, hashed_password))
        print("Created new user successfully!")

        db.commit()
        print("User data successfully added!")
            
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {e}")
        isError = True
    finally:
        cursor.close()
        db.close()
    return "User created successfully!" if not isError else "Error creating user!"