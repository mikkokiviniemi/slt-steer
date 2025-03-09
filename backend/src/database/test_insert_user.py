import asyncio
from db import users_collection  # Import the users_collection from db.py
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Async function to insert multiple test users
async def insert_test_users():
    test_users = [
        {
            "patientId": "P1001",
            "firstName": "John",
            "lastName": "Doe",
            "dateOfBirth": "1990-05-15",
            "languageSettings": {
                "preferredLanguage": "English",
                "availableLanguages": ["English", "Finnish"]
            },
            "weight": 70,
            "height": 175,
            "chatHistory": []
        },
        {
            "patientId": "P1002",
            "firstName": "Jane",
            "lastName": "Smith",
            "dateOfBirth": "1985-07-20",
            "languageSettings": {
                "preferredLanguage": "Finnish",
                "availableLanguages": ["Finnish", "Swedish"]
            },
            "weight": 65,
            "height": 168,
            "chatHistory": []
        }
    ]

    for user in test_users:
        existing_user = await users_collection.find_one({"patientId": user["patientId"]})
        if existing_user:
            logger.info(f"🔄 User {user['patientId']} already exists. Skipping insert.")
        else:
            await users_collection.insert_one(user)
            logger.info(f"✅ Test user {user['patientId']} inserted successfully!")

# Run the insert function
asyncio.run(insert_test_users())
