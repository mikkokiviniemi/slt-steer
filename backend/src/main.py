from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routes.users import router as user_router
#from ai_model import rag_cloud
from ai_model import gemini_rag_model
from ai_model import utils
from bson import ObjectId
from database.db import users_collection

app = FastAPI()
rag_system = gemini_rag_model.RAGSystem()


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
async def send_message(request: dict):
    """
    1) Lukee frontendiltä tulevan 'message' ja (optionaalisen) 'user_id' -kentän.
    2) Jos user_id on annettu ja kelvollinen, hakee käyttäjädatan MongoDB:stä.
    3) Yhdistää käyttäjädatan promtiin ja kutsuu RAG-mallia.
    """
    user_message = request.get("message")
   # user_id = request.get("user_id")  # <-- user_id voi olla mukana requestissa
    user_id = "67dcee7f8c956f5a6d144f29" # Kova koodattu tupakoitsija (meikä :D), testausta varten saa poistaa kun kirjautuminen toteutettu

    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required.")

    # 1) Haetaan käyttäjädata, jos user_id on annettu
    user_data = None
    if user_id:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid user_id format.")
        user_doc = await users_collection.find_one({"_id": ObjectId(user_id)})
        if user_doc:
            user_doc["_id"] = str(user_doc["_id"])  # Muunnetaan _id stringiksi
            user_data = user_doc

    # 2) Rakennetaan prompt, jossa lisätään käyttäjädata mukaan
    if user_data:
        prompt = f"{user_message}\n\nUser data:\n{user_data}"
    else:
        prompt = user_message

    # 3) Kutsutaan RAG-mallia
    try:
        raw_response = rag_system.get_response(prompt)
        formatted_text = utils.formatGeminiResponse(raw_response)
        return {"reply": formatted_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Register user routes
app.include_router(user_router, prefix="/users", tags=["users"])
