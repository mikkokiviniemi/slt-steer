import os
import asyncio
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import logging

# Handles MongoDB connection

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.env"))
if not os.path.exists(dotenv_path):
    logger.error(f"❌ ERROR: .env file not found at {dotenv_path}")
else:
    load_dotenv(dotenv_path)
    logger.info(f"✅ .env loaded from: {dotenv_path}")

# Get MongoDB URI
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("❌ ERROR: MONGO_URI is not set in .env file!")

logger.info(f"Loaded MONGO_URI: {MONGO_URI}")

# Connect to MongoDB
try:
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["chatbot_database"]  # Use the correct database name
    users_collection = db["users"]
    logger.info("✅ Successfully connected to MongoDB!")
except Exception as e:
    logger.error(f"❌ ERROR: Failed to connect to MongoDB: {e}")
    raise

# Expose db and users_collection for other modules
__all__ = ["db", "users_collection"]