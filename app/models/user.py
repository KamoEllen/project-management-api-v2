from pydantic import BaseModel
from app.utils import get_password_hash
from app.database import user_collection

class UserBase(BaseModel):
    """ Base model for User """
    username: str

class UserCreate(UserBase):
    """ Model for creating a user """
    password: str

class User(UserBase):
    """ Class to represent a User """
    id: str

    class Config:
        """ Pydantic configuration for user """
        from_attributes = True

def user_helper(user) -> dict:
    """ Helper function to transform user document into dictionary """
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "password": user["password"]
    }

async def create_user(user: UserCreate):
    """ Creates a new user """
    user_dict = user.dict()
    user_dict['password'] = get_password_hash(user_dict['password'])
    new_user = await user_collection.insert_one(user_dict)
    return user_helper(await user_collection.find_one({"_id": new_user.inserted_id}))

async def get_user_by_username(username: str):
    """ Function that gets a user by username """
    user = await user_collection.find_one({"username": username})
    if user:
        return user_helper(user)
    return None
