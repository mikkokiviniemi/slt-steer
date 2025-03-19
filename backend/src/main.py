from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from logging_config import logger, log_event

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

def home(request: Request):
    log_event("200 OK", "Root endpoint accessed", request)
    return {"message": "Hello from FastAPI!"}

@app.get("/api/data")
def get_data(request: Request):
    log_event("200 OK", "Data endpoint accessed", request)
    return {"data": ["Sydän", "Help help", "Ai pöhinä"]}

    
@app.post("/api/send")
def send_message(request: Request, message_request: MessageRequest):
    try:
        raw_response = get_rag_response(message_request.message)
        log_event("200 OK", "Message processed successfully", request)
        return {"reply": raw_response}
    except Exception as e:
        log_event("500 Internal Server Error", "RAG response failed", request, error_details=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")