from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

# Password Context (not needed for hardcoded credentials)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def authenticate_user(username: str, password: str):
    """ 
    Authenticate the user by verifying the username and password.
    """
    if username == HARD_CODED_USERNAME and password == HARD_CODED_PASSWORD:
        return {"username": username}
    return False

def create_access_token(data: dict, expires_delta: timedelta = None):
    """ 
    Create a JWT access token with an expiration time.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """ 
    Retrieve the current user based on the provided JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials. The token may be invalid or expired.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # Skip the user retrieval from database and directly return the hardcoded user
    if username != HARD_CODED_USERNAME:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User associated with the token does not exist. Please re-authenticate.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return {"username": username}

def verify_password(plain_password: str, hashed_password: str):
    """ 
    Verify a plain password against a hashed password.
    """
    return plain_password == hashed_password
