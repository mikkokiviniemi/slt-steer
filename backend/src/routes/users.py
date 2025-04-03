import logging
from fastapi import APIRouter, HTTPException
from database.db import users_collection
from database.models import UserModel
from bson import ObjectId

from fastapi import Request

router = APIRouter()
logging.basicConfig(level=logging.INFO)

# Global variables for user session
logged_in = False
current_user_id = None
current_user_data = None


@router.post("/login")
async def check_user_id(user_data: dict, request: Request):  # Lisätty Request-parametri
    """
    Kirjautuu sisään käyttäjänä, joka on jo olemassa MongoDB:ssä.
    Tarkistaa onko käyttäjä olemassa ja palauttaa käyttäjätiedot.
    Jos käyttäjää ei löydy, palauttaa virheilmoituksen.
    """
    
    # Set global variables
    global logged_in, current_user_id, current_user_data

    try:
        user_id = user_data.get("user_id")
        
        if not ObjectId.is_valid(user_id):
            return {"status": "error", "message": "invalid_id"}

        # tekee saman työn kuin main.py:ssä
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        
        if not user:
            return {"status": "error", "message": "not_found"}

        user["_id"] = str(user["_id"])
        
        # Päivitä  globaalit muuttujat JA sovelluksen tila
        logged_in = True
        current_user_id = user["_id"]
        current_user_data = user
        request.app.state.logged_in = True  # <-- Tallenna sovelluksen tilaan eli mainiin
        request.app.state.current_user_id = user["_id"]
        request.app.state.current_user_data = user

        logging.info(f"User logged in: {user}")
        return {"status": "success", "user": user, "message": "success"}

    except Exception as e:
        logging.exception("Login error")
        return {"status": "error", "message": "server_error"}


# Create new user to MongoDB, returns unique dataId
@router.post("/", response_model=dict)
async def create_user(user: UserModel):
    try:
        user_dict = user.model_dump() 
        result = await users_collection.insert_one(user_dict)
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to insert user.")

        # Convert ObjectId to string
        object_id = str(result.inserted_id)
        logging.info(f"✅ User saved with ObjectId: {object_id}")
        return {"user_id": object_id, "message": "User created successfully"}
    
    except Exception as e:
        logging.exception("❌ Unexpected error occurred while creating user")
        raise HTTPException(status_code=500, detail="An internal error occurred. Please try again later.")

# Get user by userId
""""
@router.get("/{user_id}", response_model=UserModel)
async def get_user(user_id: str):
    user = await users_collection.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
"""


# Modify user data
""""
@router.put("/{user_id}", response_model=UserModel)
async def update_user(user_id: str, user: UserModel):
    existing_user = await users_collection.find_one({"user_id": user_id})

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    await users_collection.update_one({"user_id": user_id}, {"$set": user.model_dump()})
    return user
"""

# Delete user by userId
""""
@router.delete("/{user_id}")
async def delete_user(user_id: str):
    delete_result = await users_collection.delete_one({"user_id": user_id})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
"""

@router.get("/id/{user_id}")
async def get_user_by_object_id(user_id: str):
    """
    Hakee user-dokumentin MongoDB:stä _id-kentän perusteella.
    Palauttaa kaiken dokumentista JSON-muodossa.
    """
    try:
        # Tarkistetaan onko user_id validi ObjectId
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid user_id format.")

        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user["_id"] = str(user["_id"])
        return user

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
