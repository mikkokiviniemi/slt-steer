from fastapi import FastAPI, HTTPException, Request, logger
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
import re
import json
import datetime
import keyring
import config
import json

app = FastAPI()

# CORS (Allow frontend to communicate with backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    message: str

# Logituksen tallennusfunktio
def log_request(request: Request = None, status: str = "200 OK", description: str = "", error_details: str = None):
    timestamp = datetime.datetime.now().strftime("%d.%m.%Y,%H:%M:%S.%f")[:-3]  # Muotoillaan aikaleima
    log_entry = {
        "timestamp": timestamp,
        "method": request.method if request else "SYSTEM",
        "url": str(request.url) if request else "SYSTEM",
        "client": request.client.host if request and request.client else "unknown",
        "status": status,
        "description": description,
        "error_details": error_details
    }

    with open("log.json", "a", encoding="utf-8") as log_file:
        json.dump(log_entry, log_file, ensure_ascii=False)
        log_file.write("\n")


# Yritetään hakea API-avain ja konfiguroida Gemini
try:
    api_key = keyring.get_password(config.SERVICE_NAME, config.USERNAME)
    if not api_key:
        raise RuntimeError("API key not found. Run 'python set_api_key.py' first.")
    genai.configure(api_key=api_key)
    log_request(status="200 OK", description="Gemini API key configured successfully")  # Lokitetaan onnistuminen

except Exception as e:
    log_request(status="500 Internal Server Error", description="Error accessing API key", error_details=str(e))
    raise RuntimeError(f"Error accessing API key: {e}")

# everyone needs to have their own service and usernames in config.py
# config.py is located in backend/src/config.py
# config.py should look like this:
#
# SERVICE_NAME = "my_gemini_service"  # Choose a descriptive name
# USERNAME = "gemini_user"         # Choose a username
#
# add config.py to .gitignore
# everyone can have their own service and usernames


# vanha API versio
# genai.configure(api_key=os.environ['gemini-api'])

# Gemini vastauksen käsittelyä luettavammaksi
def formatGeminiResponse(text: str) -> str:
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    lines = text.split("\n")
    for i, line in enumerate(lines):
        match = re.match(r'^\*\s+(.*?)$', line)
        if match:
            lines[i] = f"- {match.group(1)}"
    return "<br>".join(lines)


@app.post("/api/send")
def send_message(request: Request, message_request: MessageRequest):
    """ Käsittelee viestin ja palauttaa vastauksen """
    user_message = message_request.message
    model = genai.GenerativeModel('gemini-1.5-flash-002')
    
    try:
        response = model.generate_content(user_message)
    except Exception as e:
        log_request(request, "500 Internal Server Error", "Gemini API request failed", str(e))
        raise HTTPException(status_code=500, detail="Gemini API error")

    try:
        formatted_text = formatGeminiResponse(response.text)
    except ValueError as e:
        log_request(request, "500 Internal Server Error", "Response formatting failed", str(e))
        raise HTTPException(status_code=500, detail="Response formatting error")

    log_request(request, "200 OK", "Message processed successfully")
    return {"reply": formatted_text}
