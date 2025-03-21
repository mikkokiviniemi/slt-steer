from pydantic import BaseModel, Field
from typing import List

class UserModel(BaseModel):
    weight: float
    height: float
    conditions: List[str] = []
    avg_blood_pressure: str
    risk_factors: List[str] = []
    alcohol_use: str
    allergies: List[str] = []
    activity: str
    medications: List[str] = []
    heart_procedures: List[str] = []