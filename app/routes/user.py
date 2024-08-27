from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.models.user import User, UserCreate
from app.routes.auth import create_access_token

router = APIRouter()

# Hardcoded credentials
HARD_CODED_USERNAME = "Kamogelo"
HARD_CODED_PASSWORD = "Password123"


@router.post("/token", response_model=dict, tags=["Acess Token"])

async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """ 
    This endpoint allows users to login and receive an access token
    """
    if form_data.username != HARD_CODED_USERNAME or form_data.password != HARD_CODED_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/", response_model=User, tags=["Register Team Member"])

async def register_user(user: UserCreate):
    """ 
    This endpoint allows new users to register
    """
    if user.username == HARD_CODED_USERNAME:
        raise HTTPException(status_code=400, detail="Username already registered")
    return {"id": "unique_user_id", "username": user.username}
