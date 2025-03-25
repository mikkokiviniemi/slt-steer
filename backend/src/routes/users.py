import logging
from fastapi import APIRouter, HTTPException
from database.db import users_collection
from database.models import UserModel

router = APIRouter()
logging.basicConfig(level=logging.INFO)

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