from fastapi import APIRouter, HTTPException
from database.db import users_collection
from database.models import UserModel

router = APIRouter()

@router.post("/", response_model=UserModel)
async def create_or_update_user(user: UserModel):
    """ Adds or updates a user in MongoDB """
    existing_user = await users_collection.find_one({"patientId": user.patientId})

    if existing_user:
        await users_collection.update_one({"patientId": user.patientId}, {"$set": user.model_dump()})
    else:
        await users_collection.insert_one(user.model_dump())

    return user

@router.get("/{patientId}", response_model=UserModel)
async def get_user(patientId: str):
    """ Retrieves user data """
    user = await users_collection.find_one({"patientId": patientId})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{patientId}")
async def delete_user(patientId: str):
    """ Deletes user from MongoDB """
    delete_result = await users_collection.delete_one({"patientId": patientId})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
