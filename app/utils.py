from passlib.context import CryptContext

# Initialize CryptContext for password hashing and verification
# Using bcrypt for secure hashing; 'auto' allows for automatic detection of deprecated schemes.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """
    Verify if the provided plain password matches the stored hashed password.
    
    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.
        
    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Generate a hashed version of the provided plain password using bcrypt.
    
    Args:
        password (str): The plain text password to hash.
        
    Returns:
        str: The bcrypt hashed password.
    """
    return pwd_context.hash(password)
