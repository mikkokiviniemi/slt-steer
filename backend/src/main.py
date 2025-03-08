from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from routes.users import router as user_router
import os
import re

# Importataan RAG-funktio
from rag_cloud import get_rag_response

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

# Yksinkertainen HTML-formatoija, jos haluat säilyttää samaa logiikkaa
def formatGeminiResponse(text: str) -> str:
    # Lihavoi **merkinnät**
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Muunna markdown-listat HTML-listoiksi
    lines = text.split("\n")
    for i, line in enumerate(lines):
        match = re.match(r'^\*\s+(.*?)$', line)
        if match:
            lines[i] = f"- {match.group(1)}"

    return "<br>".join(lines)

@app.get("/")
def home():
    return {"message": "Hello from FastAPI!"}

@app.get("/api/data")
def get_data():
    return {"data": ["Sydän", "Help help", "Ai pöhinä"]}

@app.post("/api/send")
def send_message(request: MessageRequest):
    """ Käsittelee viestin ja palauttaa RAG-pohjaisen vastauksen """
    user_message = request.message
    try:
        # Käytetään RAG-ketjun vastausta
        raw_response = get_rag_response(user_message)
        formatted_text = formatGeminiResponse(raw_response)
        return {"reply": formatted_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Register user routes
app.include_router(user_router, prefix="/users", tags=["users"])
