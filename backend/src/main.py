from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from dataclasses import Field
from motor.motor_asyncio import AsyncIOMotorClient
import google.generativeai as genai
import os
import re
genai.configure(api_key=os.environ['gemini-api'])

app = FastAPI()

# CORS (Allow frontend to communicate with backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Malli viestin käsittelyä varten
class MessageRequest(BaseModel):
    message: str

# Gemini vastauksen käsittelyä luettavammaksi
def formatGeminiResponse(text: str) -> str:
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)

    lines = text.split("\n")
    for i, line in enumerate(lines):
        match = re.match(r'^\*\s+(.*?)$', line)
        if match:
            lines[i] = f"- {match.group(1)}"

    return "<br>".join(lines)

# MongoDB-yhteys
MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)
db = client["chatbot_database"]  # Tietokannan nimi
users_collection = db["users"]  # Kokoelman nimi

class MessageModel(BaseModel):
    sender: str
    message: str

class ChatHistoryModel(BaseModel):
    chatId: str
    messages: List[MessageModel]

class LanguageSettingsModel(BaseModel):
    preferredLanguage: str
    availableLanguages: List[str]

class UserModel(BaseModel):
    patientId: str = Field(..., example="P1001")
    firstName: str
    lastName: str
    dateOfBirth: str
    languageSettings: LanguageSettingsModel
    weight: int
    height: int
    chatHistory: List[ChatHistoryModel] = []
    #symptoms
    #operations

@app.get("/")
def home():
    return {"message": "Hello from FastAPI!"}

@app.get("/api/data")
def get_data():
    return {"data": ["Sydän", "Help help", "Ai pöhinä"]}

@app.post("/api/send")
def send_message(request: MessageRequest):
    """ Käsittelee viestin ja palauttaa vastauksen """
    user_message = request.message
    model = genai.GenerativeModel('gemini-1.5-flash-002')
    
    try:
        response = model.generate_content(user_message)
        #print("Raw gemini response: ", response.text)
        formatted_text = formatGeminiResponse(response.text)
        return {"reply": formatted_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/users/", response_model=UserModel)
async def create_or_update_user(user: UserModel):
    """ Lisää käyttäjän tietokantaan tai muokkaa käyttäjän tietoja """
    existing_user = await users_collection.find_one({"patientId": user.patientId})
    
    if existing_user:
        await users_collection.update_one({"patientId": user.patientId}, {"$set": user.dict()})
        return user
    else:
        await users_collection.insert_one(user.dict())
        return user

@app.get("/users/{patientId}", response_model=UserModel)
async def get_user(patientId: str):
    """ Hakee käyttäjän tiedot """
    user = await users_collection.find_one({"patientId": patientId})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{patientId}")
async def delete_user(patientId: str):
    """ Poistaa käyttäjän tietokannasta """
    delete_result = await users_collection.delete_one({"patientId": patientId})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}