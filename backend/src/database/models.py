from pydantic import BaseModel, Field
from typing import List

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