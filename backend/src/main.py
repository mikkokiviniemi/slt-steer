from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

@app.get("/")
def home():
    return {"message": "Hello from FastAPI!"}

@app.get("/api/data")
def get_data():
    return {"data": ["Sydän", "Help help", "Ai pöhinä"]}

@app.get("/api/gemini")
def get_gemini_response(question: str):
    model = genai.GenerativeModel('gemini-1.5-flash-002')
    response = model.generate_content(question)

    return {"response": response.text}
