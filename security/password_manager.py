from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Initialize the hasher with standard production profiles
ph = PasswordHasher()

def hash_new_password(plaintext_password: str) -> str:
    """
    Hash a plaintext password before saving it to PostgreSQL.
    Returns a secure string starting with '$argon2id$...'
    """
    # The library automatically generates a secure, random salt per password
    return ph.hash(plaintext_password)

def verify_user_password(stored_hash: str, plaintext_password: str) -> bool:
    """
    Verify an inbound login password against the hash retrieved from the database.
    """
    try:
        # Securely compares the password and hash using constant-time verification
        ph.verify(stored_hash, plaintext_password)
        
        # Optional check: Determine if the hash parameters need to be updated 
        # (e.g., if you upgrade your server hardware or Argon2 defaults change)
        if ph.check_needs_rehash(stored_hash):
            # You can handle rehashing and updating the DB here if needed
            pass
            
        return True
    except VerifyMismatchError:
        # Triggered if the password doesn't match or the hash is invalid
        return False
