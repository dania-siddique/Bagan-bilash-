from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    bio: str | None = None
    password: str

class UserProfile(BaseModel):
    username: str
    bio: str | None = None

    class Config:
        from_attributes = True 