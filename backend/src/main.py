from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

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
        return {"reply": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
