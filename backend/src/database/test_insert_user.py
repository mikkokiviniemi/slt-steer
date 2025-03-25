import asyncio
import logging
import httpx
from fastapi import FastAPI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "http://localhost:8000/users/"  

# Test users
test_users = [
    {
        "weight": 60,
        "height": 165,
        "conditions": ["asthma"],
        "avg_blood_pressure": "110/70",
        "risk_factors": [],
        "alcohol_use": "none",
        "allergies": ["dust"],
        "activity": "high",
        "medications": ["inhalers"],
        "heart_procedures": ["none"]
    },
    {
        "weight": 85,
        "height": 180,
        "conditions": ["hypertension", "diabetes"],
        "avg_blood_pressure": "130/85",
        "risk_factors": ["obesity", "smoking"],
        "alcohol_use": "low",
        "allergies": ["pollen"],
        "activity": "moderate",
        "medications": ["metformin", "beta-blockers"],
        "heart_procedures": ["angioplasty"]
    },
    {
        "weight": 70,
        "height": 175,
        "conditions": [],
        "avg_blood_pressure": "120/80",
        "risk_factors": [],
        "alcohol_use": "moderate",
        "allergies": [],
        "activity": "active",
        "medications": []
    }
]

async def test_create_users():
    async with httpx.AsyncClient() as client:
        inserted_count = 0
        for user in test_users:
            try:
                response = await client.post(API_URL, json=user)
                if response.status_code == 200:
                    user_id = response.json().get("user_id")
                    logger.info(f"✅ User created successfully with ID: {user_id}")
                    inserted_count += 1
                else:
                    logger.warning(f"⚠️ Failed to create user. Status: {response.status_code}, Detail: {response.text}")
            except Exception as e:
                logger.error(f"❌ Error sending request: {e}")

        logger.info(f"🚀 {inserted_count} users were successfully added via API.")

# Run the test function
if __name__ == "__main__":
    asyncio.run(test_create_users())
