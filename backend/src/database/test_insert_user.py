import asyncio
from db import users_collection  # Import the users_collection from db.py
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Async function to insert new test users
async def insert_test_users():
    test_users = [
        {
            "patientId": "P2001",
            "firstName": "Aino",
            "lastName": "Korhonen",
            "dateOfBirth": "1992-08-12",
            "languageSettings": {
                "preferredLanguage": "Finnish",
                "availableLanguages": ["Finnish", "English"]
            },
            "weight": 58,
            "height": 165,
            "chatHistory": []
        },
        {
            "patientId": "P2002",
            "firstName": "Elias",
            "lastName": "Mäkinen",
            "dateOfBirth": "1989-03-27",
            "languageSettings": {
                "preferredLanguage": "Finnish",
                "availableLanguages": ["Finnish", "Swedish"]
            },
            "weight": 80,
            "height": 180,
            "chatHistory": []
        },
        {
            "patientId": "P2003",
            "firstName": "Sophia",
            "lastName": "Anderson",
            "dateOfBirth": "1995-06-15",
            "languageSettings": {
                "preferredLanguage": "English",
                "availableLanguages": ["English"]
            },
            "weight": 68,
            "height": 170,
            "chatHistory": []
        },
        {
            "patientId": "P2004",
            "firstName": "Matti",
            "lastName": "Virtanen",
            "dateOfBirth": "1982-11-05",
            "languageSettings": {
                "preferredLanguage": "Finnish",
                "availableLanguages": ["Finnish"]
            },
            "weight": 90,
            "height": 185,
            "chatHistory": []
        }
    ]

    inserted_count = 0

    for user in test_users:
        existing_user = await users_collection.find_one({"patientId": user["patientId"]})
        if existing_user:
            logger.info(f"🔄 User {user['patientId']} already exists. Skipping insert.")
        else:
            await users_collection.insert_one(user)
            logger.info(f"✅ Inserted new user {user['patientId']}.")
            inserted_count += 1

    logger.info(f"🚀 {inserted_count} new users added. Existing users were kept.")

# Run the insert function
asyncio.run(insert_test_users())
