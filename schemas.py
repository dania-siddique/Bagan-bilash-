# schemas.py
from pydantic import BaseModel

class ChallengeCreate(BaseModel):
    title: str
    description: str

    class Config:
        from_attributes = True

class ParticipationCreate(BaseModel):
    username: str

    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    title: str
    description: str
    username: str

    class Config:
        from_attributes = True
        
class TransactionCreate(BaseModel):
    username: str
    amount: float
    method: str  # e.g. 'bKash', 'Card'

    class Config:
        from_attributes = True
