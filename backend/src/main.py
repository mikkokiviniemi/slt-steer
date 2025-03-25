from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routes.users import router as user_router
from ai_model import rag_cloud
from ai_model import utils

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

@app.post("/api/send")
def send_message(request: dict):
    user_message = request.get("message")
    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required.")
    try:
        raw_response = rag_cloud.get_rag_response(user_message)
        formatted_text = utils.formatGeminiResponse(raw_response)
        return {"reply": formatted_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Register user routes
app.include_router(user_router, prefix="/users", tags=["users"])
