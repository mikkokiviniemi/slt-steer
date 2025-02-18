from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
import re
import json

# everyone needs to have their own secrets.json file with their own gemini_api key
# secrets.json file should be in the same directory as main.py
# secrets.json file should have the following format:
# {
#     "gemini_api": "your_gemini_api_key_here"
# }
# sercret.json file should be added to .gitignore so it won't be pushed to the repository

try:
    with open("secrets.json", "r") as f:
        secrets = json.load(f)
        genai.configure(api_key=secrets["gemini_api"])
except FileNotFoundError:
    raise RuntimeError("secrets.json file was not found. Create file and add 'gemini_api' key.")
except KeyError:
    raise RuntimeError("'gemini_api' key is missing from the secrets.json file.")
except json.JSONDecodeError:
    raise RuntimeError("secrets.json file has an invalid JSON format.")

# old way of setting the api key
# genai.configure(api_key=os.environ['gemini-api'])

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
    text = re.sub(r'\*\*(.*?)\*\*', lambda match: match.group(1).upper(), text)

    lines = text.split("\n")
    counter = 1
    for i, line in enumerate(lines):
        match = re.match(r'^\*\s+(.*?)$', line)
        if match:
            lines[i] = f"{counter}. {match.group(1)}"
            counter += 1

    return "\n".join(lines)

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
